const { createApp } = Vue;

const TaskApp = {
  data() {
    return {
      task: {
        title: "",
      },
      tasks: [],
    };
  },
  async created() {
    await this.getTasks();
  },
  methods: {
    async sendRequest(url, method, data) {
      const myHeaders = new Headers({
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
      });

      const response = await fetch(url, {
        method: method,
        headers: myHeaders,
        body: data,
      });

      return response;
    },

    async getTasks() {
      const response = await this.sendRequest(window.location, "get");

      this.tasks = await response.json();
    },

    async createTask() {
      await this.getTasks();

      await this.sendRequest(
        window.location + "create",
        "post",
        JSON.stringify(this.task)
      );

      await this.getTasks();

      this.task.title = "";
    },

    async deleteTask(task) {
      await this.sendRequest(
        window.location + "delete",
        "post",
        JSON.stringify(task)
      );

      await this.getTasks();
    },

    async completeTask(task) {
      await this.sendRequest(
        window.location + "complete",
        "post",
        JSON.stringify(task)
      );

      await this.getTasks();
    },
  },
  delimiters: ["{", "}"],
};

createApp(TaskApp).mount("#app");

/* Este é um script JavaScript que define um componente Vue chamado TaskApp. O componente contém dados, tarefas e task, que é um objeto com uma propriedade title. A criação do componente inclui um método de ciclo de vida async created(), que é executado quando o componente é criado. Este método chama o método assíncrono getTasks() que envia uma solicitação HTTP GET para o servidor para obter a lista de tarefas. 

O componente também contém métodos assíncronos para criar, excluir e marcar tarefas como concluídas. Esses métodos usam o método sendRequest() para enviar solicitações HTTP POST ao servidor com os dados da tarefa em formato JSON. 

O componente usa a sintaxe de interpolação de chaves duplas para exibir as propriedades dos objetos task e tasks no HTML. A função createApp() do Vue é usada para criar e montar o componente no elemento com o ID "app" no DOM. 

adendo:Métodos assíncronos são funções que permitem a execução de tarefas de forma assíncrona, ou seja, enquanto a tarefa está sendo processada, outras tarefas podem ser executadas. No JavaScript, as funções assíncronas são definidas com a palavra-chave async e retornam uma Promise. Dentro dessas funções, é possível usar a palavra-chave await para aguardar a resolução de outras promessas ou a execução de operações assíncronas, como requisições HTTP ou acesso a bancos de dados, sem bloquear a execução do código. Isso permite que a aplicação continue respondendo a outras ações do usuário enquanto as operações assíncronas são executadas em segundo plano.

*/
