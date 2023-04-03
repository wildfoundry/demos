<script>
import axios from 'axios'
import { useMainStore } from '@/stores/main'
import TaskCreationForm from './TaskCreationForm.vue'
import Task from './Task.vue'


export default {
    setup() {
        const store = useMainStore()
        return { store }
    },
    components: {
        TaskCreationForm,
        Task,
    },
    data() {
        return {
            tasks: [],
        }
    },
    methods: {
        async getTasks() {
            try {
                const response = await axios.get(
                    this.store.baseAPIURL + "scrum/tasks/",
                    { auth: {username: this.store.username, password: this.store.password}}
                );
                this.tasks = response.data;
                console.log(this.tasks);
            } catch (e) {
                console.error(e.response.data)
            }
        }
    },
    mounted() {
        this.getTasks()
    },
    computed: {
        tasksTD() {
            return this.tasks.filter((task) => task.stage == 'TD')
        },
        tasksIP() {
            return this.tasks.filter((task) => task.stage == 'IP')
        },
        tasksDN() {
            return this.tasks.filter((task) => task.stage == 'DN')
        },
    }
}
</script>

<template>
    <div class="container">
        <div class="stage">
            <h1>To do</h1>
            <ul class="list">
                <li v-for="task of tasksTD" :key="task.id">
                    <Task :task="task" @refreshTasks="getTasks" />
                </li>
            </ul>
            <TaskCreationForm @refreshTasks="getTasks" stage="TD"  />
        </div>
        <div class="stage">
            <h1>In progress</h1>
            <ul class="list">
                <li v-for="task of tasksIP" :key="task.id">
                    <Task :task="task" @refreshTasks="getTasks" />
                </li>
            </ul>
            <TaskCreationForm @refreshTasks="getTasks" stage="IP" />
        </div>
        <div class="stage">
            <h1>Done</h1>
            <ul class="list">
                <li v-for="task of tasksDN" :key="task.id">
                    <Task :task="task" @refreshTasks="getTasks" />
                </li>
            </ul>
            <TaskCreationForm @refreshTasks="getTasks" stage="DN" />
        </div>    
    </div>
</template>

<style scoped>
.stage {
    text-align: center;
    width: 33%;
    float: left;
    margin-top: 10px;
}
.list {
    list-style: none;
}
</style>