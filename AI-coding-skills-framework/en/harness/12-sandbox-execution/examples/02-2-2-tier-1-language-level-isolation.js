const vm = require("node:vm");
const ctx = vm.createContext({ /* nothing inherited */ });
vm.runInContext("this.constructor.constructor('return process')()", ctx);
