from domain.category import Category
from shared.event_dispatcher import dispatcher
# Importar handlers para garantir que sejam registrados
import app.event_handlers

print("--- Criando uma nova categoria ---")
category1 = Category(name="Eletrônicos", description="Produtos eletrônicos em geral")
print(f"Categoria criada: {category1}")
# Disparar eventos após a operação de domínio ser concluída e persistida(simulado)
for event in category1.clear_domain_events():
    dispatcher.dispatch(event)

print("\n--- Atualizando a categoria ---")
category1.update(name="Eletrônicos Modernos", description="Dispositivos eletrônicos de última geração")
print(f"Categoria atualizada: {category1}")

for event in category1.clear_domain_events():
    dispatcher.dispatch(event)

print("\n--- Desativando a categoria ---")
category1.deactivate()
print(f"Categoria desativada: {category1}")
for event in category1.clear_domain_events():
    dispatcher.dispatch(event)

print("\n--- Ativando a categoria ---")
category1.activate()
print(f"Categoria ativada: {category1}")

for event in category1.clear_domain_events():
    dispatcher.dispatch(event)
print("\n--- Tentando desativar novamente (não deve disparar evento) ---")
category1.deactivate()
print(f"Categoria desativada: {category1}")
# Não haverá eventos para disparar aqui, pois o estado não mudou
for event in category1.clear_domain_events():
    dispatcher.dispatch(event)
