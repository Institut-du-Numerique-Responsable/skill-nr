#!/usr/bin/env python3
"""Régressions du préfiltre : index Git, chemins, commentaires et langages."""
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

AUDIT = Path(__file__).resolve().with_name('eco-audit.sh')


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='nr-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.git('init', '-q')
        self.git('config', 'core.quotePath', 'true')

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, check=True,
                              capture_output=True, text=True).stdout

    def audit(self, *args):
        return subprocess.run(['bash', str(AUDIT), *args], cwd=self.root,
                              capture_output=True, text=True)

    def write(self, name, content):
        (self.root / name).write_text(content)

    def test_index_is_audited_in_both_directions(self):
        for staged, working, expected in [
            ('SELECT * FROM t;', 'SELECT id FROM t;', 1),
            ('SELECT id FROM t;', 'SELECT * FROM t;', 0),
        ]:
            with self.subTest(staged=staged):
                self.write('query.sql', staged)
                self.git('add', 'query.sql')
                self.write('query.sql', working)
                self.assertEqual(self.audit('--index').returncode, expected)
                self.assertEqual(self.audit().returncode, expected)
                self.assertEqual(self.audit('query.sql').returncode, 1 - expected)
        (self.root / 'query.sql').unlink()
        self.assertEqual(self.audit('--index').returncode, 0)

    def test_automatic_paths(self):
        for name in ['requête.sql', 'avec espaces.sql', 'tab\t.sql',
                     'ligne\n.sql', '--help.sql', '[motif].sql']:
            with self.subTest(name=name):
                self.write(name, 'SELECT * FROM t;')
                self.git('add', '--', name)
        result = self.audit()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('6 élevé(s)', result.stdout)
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                 'commit', '-qm', 'fixtures')
        self.assertEqual(self.audit('--index').returncode, 0)
        self.assertIn('6 élevé(s)', self.audit('--depot').stdout)
        self.assertIn('6 élevé(s)', self.audit().stdout)

    def test_comments_and_line_numbers(self):
        self.write('query.sql', '-- SELECT * FROM t;\n/* SELECT *\nFROM t; */\nSELECT id FROM t;\nSELECT * FROM t;\n')
        result = self.audit('query.sql')
        self.assertEqual(result.returncode, 1)
        self.assertIn('query.sql:5 [Élevé]', result.stdout)
        self.assertIn('1 élevé(s)', result.stdout)
        self.write('query.sql', "SELECT '-- /*' AS value; -- SELECT * FROM t;\nSELECT id FROM t;\n")
        self.assertEqual(self.audit('query.sql').returncode, 0)
        self.write('page.html', '<!-- <video autoplay>\n<img src="a.jpg"> -->\n<p>Texte</p>\n')
        self.assertEqual(self.audit('page.html').returncode, 0)

    def test_comment_delimiters_in_strings(self):
        self.write('page.html', "<p>L'image est citée</p>\n<!-- <video autoplay> -->\n")
        self.assertEqual(self.audit('page.html').returncode, 0)
        self.write('query.sql', "/* externe /* interne */ SELECT * FROM t; */\nSELECT id FROM t;\n")
        self.assertEqual(self.audit('query.sql').returncode, 0)
        self.write('query.sql', "SELECT $$-- pas un commentaire$$; SELECT * FROM t;\n")
        self.assertEqual(self.audit('query.sql').returncode, 1)

    def test_python_strings_keep_comment_delimiters(self):
        pattern = json.loads((AUDIT.parent.parent / 'verification/eco-audit-cases.json').read_text())['py'][0]
        self.write('sample.py', '# ' + pattern + '\nvalue = "# preserved"\n')
        self.assertEqual(self.audit('sample.py').returncode, 0)
        self.write('sample.py', 'value = "# preserved"\n' + pattern + '\n')
        result = self.audit('sample.py')
        self.assertEqual(result.returncode, 1)
        self.assertIn('sample.py:2', result.stdout)

    def test_unsupported_extension_skips_processing(self):
        # Un interpréteur factice signale toute tentative de traitement inutile.
        fake = self.root / 'python3'
        fake.write_text('#!/bin/sh\nexit 99\n')
        fake.chmod(0o755)
        self.write('asset.png', 'not source code')
        result = subprocess.run(['bash', str(AUDIT), 'asset.png'], cwd=self.root,
                                env={**os.environ, 'PATH': str(self.root) + os.pathsep + os.environ['PATH']},
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_language_pairs(self):
        # Une paire fautive/conforme par famille, sans prétendre couvrir tous les motifs.
        pairs = json.loads((AUDIT.parent.parent / 'verification/eco-audit-cases.json').read_text())
        for ext, (bad, good) in pairs.items():
            with self.subTest(language=ext):
                name = 'sample.' + ext
                self.write(name, bad + '\n')
                self.assertIn('[', self.audit(name).stdout)
                self.write(name, good + '\n')
                self.assertIn('aucun motif connu', self.audit(name).stdout)

    def test_missing_file_is_an_error_even_when_warning(self):
        self.assertEqual(self.audit('--avertir', 'absent.sql').returncode, 2)


if __name__ == '__main__':
    unittest.main()
