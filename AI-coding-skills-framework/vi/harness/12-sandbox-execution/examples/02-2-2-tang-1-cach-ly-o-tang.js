const vm = require("node:vm");
const ctx = vm.createContext({ /* không kế thừa gì */ });
vm.runInContext("this.constructor.constructor('return process')()", ctx);
