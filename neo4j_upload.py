from py2neo import Graph, Node, Relationship
import json
import yaml

def load_config(config_path):
    with open(config_path) as file:
        return yaml.safe_load(file)

def connect_to_graph(config):
    neo4j_config = config["neo4j"]
    return Graph(f"{neo4j_config['host']}:{neo4j_config['port']}", 
                 auth=(neo4j_config['user'], neo4j_config['password']))

def load_company_data(company_data_path):
    with open(company_data_path, 'r') as file:
        return json.load(file)

def upload_data_to_neo4j(graph, data):
    for info in data:
        company_info = Node("Company",
                            company_name=info["company_name"],
                            company_url=info["company_url"],
                            company_logo=info["company_logo"],
                            company_about=info["company_about"],
                            industries=info["industries"],
                            location=info["location"],
                            links=info["links"])
        graph.merge(company_info, "Company", "company_url")
        
        for person in info["persons"]:
            if person["profil_url"]:
                person_info = Node("Person",
                                   name=person["name"],
                                   role=person["role"],
                                   profil_url=person["profil_url"],
                                   photo_url=person["photo_url"],
                                   person_links=person["person_links"],
                                   person_about=person["person_about"],
                                   prev_comp_link=person["prev_comp_link"])
                graph.merge(person_info, "Person", "profil_url")
                
                relation = Relationship(person_info, "WORKING_AT", company_info, role=person["role"])
                graph.merge(relation)
        
        for team in info["teams"]:
            team_info = Node("Team",
                             team_name=team["team_name"],
                             company_url=info["company_url"])
            graph.merge(team_info, "Team", ("team_name", "company_url"))
            
            relation = Relationship(team_info, "TEAM", company_info)
            graph.merge(relation)
            
            for member in team["members"]:
                if member["profil_url"]:
                    member_info = Node("Person",
                                       name=member["name"],
                                       role=member["role"],
                                       profil_url=member["profil_url"],
                                       photo_url=member["photo_url"],
                                       person_links=member["person_links"],
                                       person_about=member["person_about"],
                                       prev_comp_link=member["prev_comp_link"])
                    graph.merge(member_info, "Person", "profil_url")
                    
                    relation = Relationship(member_info, "WORKING_AT", team_info, role=member["role"])
                    graph.merge(relation)
                    print("Başarılı: ", member["name"])

def main():
    config_path = "/config/config.yaml"
    company_data_path = "/company_data/company.json"
    
    config = load_config(config_path)
    graph = connect_to_graph(config)
    data = load_company_data(company_data_path)
    
    upload_data_to_neo4j(graph, data)
    print("BASARILI")

if __name__ == "__main__":
    main()
