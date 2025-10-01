## RESUMOS

- @static method
    
    @static method é um decorator que permite que o metodo que o prossiga possa ser chamada sem que necessariamente já tenha instanciado o objeto

- Dataclasses
    
    Dataclasses permitem criar classes com menos códigos, elas otimizam o tempo de criação, ela já cria as funções __init__, __repr__, __equal__ economizando tempo e código. Nesse trabalho foram utilizadas funcoes como Field para definir um valor padrão do atributo, já o atributo frozen=True impede que os atributos do objeto criado sejam modificados.

- Eventos de domínio
    
    Os eventos de dominio ocorre quando há uma criação, modificação ou remoção de um objeto de valor, criando um log contendo informações importantes do objeto e a data da ocorrencia. esses eventos podem ser utilizados para auditorias ou para encadear outras funções que não precisam ser incluidas no código que realizou a alteração.

- Decoradores
    
    Decoradores atribuem uma funcao para a funcao que esta sendo criada, ele vai tratar a função criada como um filho, podendo adicionar funcionalidades antes e depois de ocorrer a função

- DDD

    O DDD(domain driven design) é o desenvolvimento de uma aplicação baseada em eventos de dominio, ou seja, quando ocorrer um registro de evento, pode disparar uma ação pelo registro do evento e não dentro da função que o registrou, tornando o código modular podendo realizar alterações, ou funções sem precisar modificar o restante. por exemplo ao registrar um novo usuário é disparado um evento, com base nesse evento uma funçaão envia um email com os dados e informações para o usuário registrado. nesse formato a função de criar o usuário não chama a função de enviar o email, o tornando modular e facilitando manutebilidade e atualizações futuras, pois ao alterar em qualquer uma das funções não irá inteferir na outra.