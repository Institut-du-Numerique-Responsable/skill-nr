#!/usr/bin/env python3
"""Vérifie le paquet copiable, les références et les garde-fous de génération."""
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('generateur', ROOT / 'scripts/generer-versions.py')
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)


class GenerationTests(unittest.TestCase):
    def test_packages_and_missing_reference(self):
        with tempfile.TemporaryDirectory(prefix='nr-versions-') as temp:
            gen.OUT = Path(temp)
            gen.generer()
            for tool, entry in [('claude-code', 'CLAUDE.md'), ('gemini-cli', 'GEMINI.md'),
                                ('opencode', 'AGENTS.md'), ('mistral-vibe', 'AGENTS.md'),
                                ('kimi-cli', 'AGENTS.md')]:
                with self.subTest(tool=tool):
                    package = gen.OUT / tool
                    context = (package / entry).read_text()
                    self.assertLess(len(context.encode()), 12000)
                    self.assertIn('Accessibilité', context)
                    for slug in gen.ORDRE[2:]:
                        reference = package / '.nr/regles' / (slug + '.md')
                        self.assertIn(str(reference.relative_to(package)), context)
                        self.assertTrue(all(line in reference.read_text()
                                            for line in gen.lire_regle(slug)[1].splitlines()), str(reference))
                    command = ['bash', str(ROOT / 'scripts/verifier-installation.sh'), tool, str(package)]
                    result = subprocess.run(command, capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stdout)
                    (package / '.nr/regles/ecoconception-sql.md').unlink()
                    self.assertEqual(subprocess.run(command, capture_output=True).returncode, 1)

    def test_kilo_skills_and_installation(self):
        with tempfile.TemporaryDirectory(prefix="nr-kilo-") as temp:
            gen.OUT = Path(temp)
            gen.generer()
            package = gen.OUT / "kilo"
            skills = package / ".kilo/skills"
            self.assertEqual({p.name for p in skills.iterdir()}, set(gen.ORDRE))
            self.assertFalse((package / "kilo.jsonc").exists())
            self.assertFalse((package / ".kilo/rules").exists())
            for slug in gen.ORDRE:
                texte = (skills / slug / "SKILL.md").read_text()
                frontmatter = texte.split("---", 2)[1].strip().splitlines()
                self.assertEqual(frontmatter[0], "name: " + slug)
                description = json.loads(frontmatter[1].removeprefix("description: "))
                self.assertTrue(0 < len(description) <= 1024)
                self.assertNotIn("TEMPO", texte)
                self.assertNotIn("BPCE", texte)
                self.assertIn("CC-BY-SA-4.0", texte)
            usage = (skills / "usage-sobre-assistant/SKILL.md").read_text()
            self.assertIn("Qualité et mesure", usage)
            self.assertNotIn("ordre de grandeur de moins", usage)
            self.assertNotIn("retire de `kilo.jsonc`", usage)
            command = ["bash", str(ROOT / "scripts/verifier-installation.sh"), "kilo", str(package)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout)
            source = skills / "ecoconception-python/SKILL.md"
            original = source.read_text()
            source.write_text(original.replace("name: ecoconception-python", "name: mauvais-nom"))
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 1)
            source.write_text(original)
            (skills / "ecoconception-sql/SKILL.md").unlink()
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 1)


if __name__ == '__main__':
    unittest.main()
