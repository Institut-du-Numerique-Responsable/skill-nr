public class CommandeService
{
    private readonly AppDbContext _db;

    public List<CommandeDto> GetCommandesClient(int clientId)
    {
        var commandes = _db.Commandes.ToList()
            .Where(c => c.ClientId == clientId)
            .ToList();

        var result = new List<CommandeDto>();
        foreach (var commande in commandes)
        {
            if (commande.Lignes.Count() > 0)
            {
                var client = new HttpClient();
                var statut = client.GetStringAsync($"https://api.interne/statut/{commande.Id}").Result;
                result.Add(new CommandeDto { Id = commande.Id, Statut = statut, Lignes = commande.Lignes });
            }
        }
        return result;
    }
}
