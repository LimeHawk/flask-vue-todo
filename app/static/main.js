const { createApp } = Vue;

const TaskApp = {
  data() {
    return {
      task: "",
      tasks: [{ title: "One" }, { title: "Two" }],
    };
  },
  delimiters: ["{", "}"],
};

createApp(TaskApp).mount("#app");
