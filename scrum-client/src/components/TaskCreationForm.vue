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
            name: "",
            description: "",
            priority: "",
        }
    },
    props : {
        stage: String
    },
    emits: ['refreshTasks'],
    methods: {
        async addTask() {
            try {
                const response = await axios.post(
                    this.store.baseAPIURL + "scrum/tasks/",
                    { name: this.name, description: this.description, stage: this.stage, priority: this.priority },
                    { auth: {username: this.store.username, password: this.store.password}}
                );
                this.$emit('refreshTasks');
            } catch (e) {
                console.error(e)
            }
            
            this.name = ""
            this.description = ""
        }
    }
}
</script>

<template>
    <form @submit.prevent="addTask">
        <h3>Create task:</h3>
        <input type="text" placeholder="name" v-model="name">
        <input type="text" placeholder="description" v-model="description">
        <label for="priorities"> Priority: </label>
        <select class="dropdown" name="priorities" v-model="priority">
            <option value="L">Low</option>
            <option value="M">Medium</option>
            <option value="H">High</option>
        </select>
        <input class="btn" type="submit" value="Create task">
    </form>
</template>