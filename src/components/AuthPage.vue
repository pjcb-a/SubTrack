<script setup>

</script>

<template>
  <div class="auth-container">
    <div class="auth-card" :class="{ 'flex-reverse': !isLogin }">
      
      <div class="info-panel">
        <div v-if="isLogin">
          <h1>Welcome To SubTrack</h1>
          <p>Login with username and password</p>
          <button @click="isLogin = false" class="ghost-btn">Login</button>
        </div>
        <div v-else>
          <h1>Back On Track</h1>
          <p>Register now and enjoy our site</p>
          <button @click="isLogin = true" class="ghost-btn">Register</button>
        </div>
      </div>

      <div class="form-panel">
        <h1>{{ isLogin ? 'Login' : 'Register' }}</h1>
        
        <div class="input-group">
          <label>Username</label>
          <input type="text" v-model="form.username" />
        </div>

        <div v-if="!isLogin" class="input-group">
          <label>Email</label>
          <input type="email" v-model="form.email" />
        </div>

        <div class="input-group">
          <label>Password</label>
          <input type="password" v-model="form.password" />
        </div>

        <button class="submit-btn">
          {{ isLogin ? 'Login' : 'Register' }}
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

const isLogin = ref(true);

const form = reactive({
  username: '',
  email: '',
  password: ''
});
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  font-family: 'Arial', sans-serif;
}

.auth-card {
  display: flex;
  width: 800px;
  height: 500px;
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  transition: all 0.5s ease;
}

.flex-reverse {
  flex-direction: row-reverse;
}

.info-panel {
  flex: 1;
  background-color: #1e5628; /* Forest Green */
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 40px;
  gap: 1rem;
}

.info-panel h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.form-panel {
  flex: 1;
  padding: 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.form-panel h1 {
  font-size: 2rem;
  margin-bottom: 30px;
  text-align: center;
  color:#1e5628;
}

.input-group {
  margin-bottom: 15px;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.input-group input {
  width: 100%;
  padding: 12px;
  border: none;
  background-color: #d9d9d9;
  border-radius: 8px;
  outline: none;
}

.submit-btn, .ghost-btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  margin-top: 10px;
  transition: opacity 0.2s;
}

.submit-btn {
  background-color: #cccccc;
  color: #333;
}

.ghost-btn {
  background-color: #cccccc;
  color: #333;
  width: 150px;
}

.submit-btn:hover, .ghost-btn:hover {
  opacity: 0.8;
}
</style>