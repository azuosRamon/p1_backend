from events.category_events import CategoryCreated, CategoryUpdated, CategoryActivated, CategoryDeactivated
from shared.event_dispatcher import dispatcher

def log_category_creation(event: CategoryCreated) -> None:
    print(f"[LOG] Categoria Criada: {event.name} (ID: {event.category_id})")
    # Ex: Enviar para um sistema de log externo

def log_category_update(event: CategoryUpdated) -> None:
    print(f"[LOG] Categoria Atualizada: ID {event.category_id} | Nome:'{event.old_name}' -> '{event.new_name}'")
    # Ex: Invalidar cache relacionado à categoria

def send_notification_on_deactivation(event: CategoryDeactivated) -> None:
    print(f"[NOTIFICATION] Categoria ID {event.category_id} foi desativada. Notificar administradores.")
    # Ex: Enviar e-mail para administradores

def update_search_index_on_activation(event: CategoryActivated) -> None:
    print(f"[SEARCH_INDEX] Categoria ID {event.category_id} ativada. Atualizar índice de busca.")
    # Ex: Chamar API de serviço de busca

# Registrar os handlers no dispatcher
dispatcher.register_handler(CategoryCreated, log_category_creation)
dispatcher.register_handler(CategoryUpdated, log_category_update)
dispatcher.register_handler(CategoryDeactivated, send_notification_on_deactivation)
dispatcher.register_handler(CategoryActivated, update_search_index_on_activation)