@Service
public class ClientService {

    private static final Map<Long, Client> CACHE = new HashMap<>();

    @Autowired
    private ClientRepository clientRepository;

    public String rapportOperations() {
        String rapport = "";
        List<Client> clients = clientRepository.findAll();
        for (Client client : clients) {
            log.info("Traitement du client " + client.getNom());
            CACHE.put(client.getId(), client);
            for (Operation op : client.getOperations()) {
                rapport += client.getNom() + ";" + op.getMontant() + "\n";
            }
        }
        return rapport;
    }

    public List<Client> rechercher() {
        return clientRepository.findAll().parallelStream()
            .filter(c -> c.isActif())
            .collect(Collectors.toList());
    }
}
