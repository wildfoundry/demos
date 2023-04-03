<script>
import axios from 'axios'
import { useMainStore } from '@/stores/main'
import TaskEditionForm from './TaskEditionForm.vue'


export default {
    setup() {
        const store = useMainStore()
        return { store }
    },
    data() {
        return {
            editing: false,
        }
    },
    components: {
        TaskEditionForm,
    },
    props: {
        task: {},
    },
    emits: ['refreshTasks'],
    methods: {
        async deleteTask() {
            try {
                await axios.delete(
                    this.store.baseAPIURL + 'scrum/tasks/' + this.task.id + '/',
                    { auth: {username: this.store.username, password: this.store.password } }
                );
                this.$emit('refreshTasks')
            } catch (e) {
                console.error(e.response.data)
            }
        },
        editTask() {
            this.editing = true
        }
    }
}
</script>

<template>
    <div class="task_container" v-if="!editing">
        <div class="task_internals">
            <h2>{{ task.name }}</h2>
            <div>{{ task.description }}</div>
            <button class="btn" @click="editTask">Edit</button>
            <button class="btn" @click="deleteTask">Delete</button>
        </div>
        <div class="priority_strip" :style="{'background-color': task.priority=='L' ? '#5CD470' : 
    task.priority=='M' ? '#5CBED4' : '#D45C6A'}"></div>
    </div>
    <TaskEditionForm :task="task" @refreshTasks="this.$emit('refreshTasks'); this.editing=false" v-else />
</template>

<style scoped>
    .task_container {
        background-color: rgb(240, 252, 185);
        margin: 15px;
        width: 400px;
        height: 120px;
        border-radius: 10px;
        box-shadow: 5px 3px 3px black;
    }
    .task_internals {
        float: left;
        width: 380px;
    }
    .priority_strip {
        float: right;
        width: 20px;
        height: 100%;
        border-top-right-radius: 10px;
        border-bottom-right-radius: 10px;
    }
</style>