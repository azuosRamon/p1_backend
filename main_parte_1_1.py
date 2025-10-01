from domain.category import Category

print("--- Teste to_dict() e from_dict() ---")

# Criar categoria
c1 = Category(name="Games", description="Jogos em geral")
print("Original:", c1)

# Serializar
d = c1.to_dict()
print("Dicionário:", d)

# Reconstruir
c2 = Category.from_dict(d)
print("Reconstruída:", c2)

# Verificar equivalência
print("Os objetos são iguais?", c1.id == c2.id and c1.name == c2.name and c1.description == c2.description)
