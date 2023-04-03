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
            stage: this.task.stage,
        }
    },
    props : {
        task: {},
    },
    emits: ['refreshTasks'],
    methods: {
        async editTask() {
            try {
                const response = await axios.put(
                    this.store.baseAPIURL + "scrum/tasks/" + this.task.id + "/",
                    { name: this.task.name, description: this.task.description, stage: this.stage, priority: this.task.priority },
                    { auth: {username: this.store.username, password: this.store.password}}
                );
                this.$emit('refreshTasks');
            } catch (e) {
                console.error(e)
            }
        }
    }
}
</script>

<template>
    <form @submit.prevent="editTask">
        <h3>Edit task:</h3>
        <input type="text" placeholder="name" v-model="task.name">
        <input type="text" placeholder="description" v-model="task.description">
        <label for="priorities"> Priority: </label>
        <select class="dropdown" name="priorities" v-model="task.priority">
            <option value="L">Low</option>
            <option value="M">Medium</option>
            <option value="H">High</option>
        </select>
        <label for="stages"> Stage: </label>
        <select class="dropdown" name="stages" v-model="stage">
            <option value="TD">To do</option>
            <option value="IP">In progress</option>
            <option value="DN">Done</option>
        </select>
        <input class="btn" type="submit" value="Edit task">
    </form>
</template>