<script setup>
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import { useAuth } from '../../composables/useAuth';

const router = useRouter();
const identifier = ref('');
const password = ref('');
const localError = ref('');
const { login, authLoading } = useAuth();

const handleLogin = async () => {
  localError.value = '';

  if (!identifier.value.trim() || !password.value) {
    localError.value = 'Enter your username or email and password.';
    return;
  }

  try {
    await login({
      identifier: identifier.value,
      password: password.value,
    });
    router.push('/dashboard');
  } catch (error) {
    localError.value = error.message;
  }
};
</script>

<template>
  <div class="form-content">
    <div class="form-intro">
      <span class="eyebrow">Welcome back</span>
      <h1>Sign in to SubTrack</h1>
      <p>Use your username or email to access your dashboard and settings.</p>
    </div>

    <div class="input-group">
        <label for="identifier">Username or Email</label>
        <input type="text" id="identifier" v-model="identifier" placeholder="Enter username or email"/>
    </div>
    
    <div class="input-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" placeholder="Enter password" />
    </div>

    <p v-if="localError" class="form-error">{{ localError }}</p>

    <button @click="handleLogin" class="submit-btn" :disabled="authLoading">
      {{ authLoading ? 'Signing in...' : 'Sign In' }}
    </button>
  </div>
</template>

<style scoped>
.form-content {
  width: min(100%, 560px);
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 14px;
  font-family: 'Montserrat', sans-serif;
}

.form-intro {
  display: grid;
  gap: 10px;
  margin-bottom: 8px;
}

.eyebrow {
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: #6d7f97;
}

.form-content h1 {
  font-weight: 800;
  font-size: clamp(2.6rem, 4vw, 4rem);
  letter-spacing: -0.04em;
  color: var(--app-heading);
}

.form-intro p {
  color: var(--app-text-muted);
  line-height: 1.65;
}

.input-group {
  width: 100%;
  text-align: left;
}

.input-group label {
  font-family: 'Montserrat', sans-serif;
  display: block;
  padding-left: 2px;
  margin-bottom: 8px;
  font-size: 0.84rem;
  font-weight: 700;
  color: var(--app-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.input-group input {
  width: 100%;
  padding: 15px 16px;
  background: var(--app-surface);
  color: var(--app-text);
  border: 1px solid color-mix(in srgb, var(--app-border) 88%, transparent);
  border-radius: 18px;
  font-family: 'Montserrat', sans-serif;
  transition: border-color 0.25s ease, box-shadow 0.25s ease, background 0.25s ease;
}

.input-group input:focus {
  outline: none;
  border-color: var(--app-accent);
  background: #fff;
  box-shadow: 0 0 0 4px rgba(13, 106, 69, 0.1);
}

.submit-btn {
  width: 100%;
  margin-top: 8px;
  padding: 14px 18px;
  background: linear-gradient(90deg, #0f5d3b 0%, #0d6a45 100%);
  color: #fff;
  border-radius: 18px;
  font-size: 1.05rem;
  font-weight: 700;
  border: none;
  cursor: pointer;
}

.submit-btn:hover {
  box-shadow: 0 14px 24px rgba(13, 106, 69, 0.18);
  transform: translateY(-2px);
  transition: transform 0.3s, box-shadow 0.3s;
}

.submit-btn:disabled {
  opacity: 0.75;
  cursor: wait;
}

.form-error {
  width: 100%;
  margin-top: 4px;
  color: #aa3333;
  font-size: 0.88rem;
  text-align: left;
}

@media (max-width: 960px) {
  .form-content {
    width: 100%;
  }
}
</style>
