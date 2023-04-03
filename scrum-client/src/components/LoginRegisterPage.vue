<script>
import axios from 'axios'
import { useMainStore } from '@/stores/main'


export default {
    setup() {
        const store = useMainStore()
        return { store }
    },
    data() {
        return {
            usernameLogin: "",
            passwordLogin: "",
            messageLogin: "",
            usernameRegister: "",
            passwordRegister: "",
            password2Register: "",
            messageRegister: "",
        }
    }, 
    methods: {
        async register() {
            try {
                await axios.post(this.store.baseAPIURL + "auth/register/", 
                {
                    username: this.usernameRegister,
                    password: this.passwordRegister,
                    password2: this.password2Register,
                });
                this.messageRegister = "User " + this.usernameRegister + " created"
            } catch (e) {
                this.messageRegister = e.response.data
            }
            this.usernameRegister = ""
            this.passwordRegister = ""
            this.password2Register = ""
            this.usernameLogin = ""
            this.passwordLogin = ""
            this.messageLogin = ""
        },

        async login() {
            try {
                await axios.get(
                    this.store.baseAPIURL + "scrum/tasks/",
                    { auth: {username: this.usernameLogin, password: this.passwordLogin}}
                );
                this.store.username = this.usernameLogin
                this.store.password = this.passwordLogin
            } catch (e) {
                this.messageLogin = e.response.data
                this.usernameLogin = ""
                this.passwordLogin = ""
                this.messageRegister = ""
            }
        }
    },
}
</script>

<template>
    <form @submit.prevent="login">
        <h1>Login form</h1>
        <input type="text" placeholder="username" v-model="usernameLogin">
        <input type="password" placeholder="password" v-model="passwordLogin">
        <input type="submit" value="Login">
        <div name="info">{{ messageLogin }}</div>
    </form>
    <form @submit.prevent="register">
        <h1>Register form</h1>
        <input type="text" placeholder="username" v-model="usernameRegister">
        <input type="password" placeholder="password" v-model="passwordRegister">
        <input type="password" placeholder="repeat password" v-model="password2Register">
        <input type="submit" value="Sign up">
        <div name="info">{{ messageRegister }}</div>
    </form>   
</template>