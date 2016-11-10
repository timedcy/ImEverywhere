from py2neo import Graph, Node, Relationship

graph = Graph("http://localhost:7474/db/data/", password = "102422")

credit_card = Node("Card", name = "Credit")
other_card = Node("Card", name = "Other")
deposit_card = Node("Card", name = "Deposit", service = ["current", "regular", "saving", "notice"])
bank_root = Node("Root", name = "BankingBusiness")
deposit_current = Node("Service", name = "CurrentDeposit")
deposit_regular = Node("Service", name = "RegularDeposit")
deposit_saving = Node("Service", name = "SavingDeposit")
deposit_notice = Node("Service", name = "NoticeDeposit")

credit_bank = Relationship(credit_card, "BelongTo", bank_root)
other_bank = Relationship(other_card, "BelongTo", bank_root)
deposit_bank = Relationship(deposit_card, "BelongTo", bank_root)

dcurrent = Relationship(deposit_card, "Support", deposit_current)
dregular = Relationship(deposit_card, "Support", deposit_regular)
dsaving = Relationship(deposit_card, "Support", deposit_saving)
dnotice = Relationship(deposit_card, "Support", deposit_notice)

graph.create(bank_root)
graph.create(credit_bank)
graph.create(other_bank)
graph.create(deposit_bank)

graph.create(dcurrent)
graph.create(dregular)
graph.create(dsaving)
graph.create(dnotice)

print(graph.exists(credit_bank))
print(graph.exists(deposit_bank))

query_1 = graph.data("MATCH (mycard:Card) RETURN mycard.name LIMIT 1")
print(query_1)
query_2 = graph.run("MATCH (mycard) WHERE mycard.name={x} RETURN mycard.service", x = "Deposit").evaluate()
print(query_2)
match_1 = graph.match(start_node = credit_card, rel_type = "BelongTo")
print(list(match_1)[0].end_node()["name"])
