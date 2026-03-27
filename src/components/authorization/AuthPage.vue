<script setup>
import { ref } from 'vue';
import LoginForm from './LoginForm.vue';
import RegisterForm from './RegisterForm.vue';

const isLogin = ref(false);
</script>

  <!-- Dynamic wrapper for both Register and Login page to render smoothly -->
  <template>
  <div class="auth-wrapper">
    <div class="auth-card" :class="{ 'is-register-active': !isLogin }">
      
      <div class="forms-bg-container">
        <div class="form-section login-section">
          <LoginForm />
        </div>
        <div class="form-section register-section">
          <RegisterForm />
        </div>
      </div>

      <div class="overlay-container">
        <div class="overlay">
          <div class="overlay-content">
            <h1>{{ isLogin ? 'Back on Track' : 'Welcome To SubTrack' }}</h1>
            <p>{{ isLogin ? 'Login with username and password' : 'Register now and enjoy our site' }}</p>
            <button @click="isLogin = !isLogin" class="ghost-btn">
              {{ isLogin ? 'Login' : 'Register' }}
            </button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.auth-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #1a1a1a; /* Dark background to make the card pop */
  padding: 20px;
}

.auth-card {
  position: relative;
  display: flex;
  width: 100%;
  max-width: 1000px;
  height: 600px;
  background: white;
  border-radius: 30px;
  overflow: hidden; /* Clips the forms behind the green panel */
  box-shadow: 0 15px 35px rgba(0,0,0,0.5);
}

/* This container holds both forms in a row */
.forms-bg-container {
  display: flex;
  width: 100%;
  height: 100%;
}

.form-section {
  flex: 1; /* Each takes exactly 50% */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1;
}

/* THE SLIDER */
.overlay-container {
  position: absolute;
  top: 0;
  left: 50%; /* Default position covering Register side */
  width: 50%;
  height: 100%;
  z-index: 10;
  transition: transform 0.6s ease-in-out;
}

/* Move left to cover Login side when Registering */
.is-register-active .overlay-container {
  transform: translateX(-100%);
}

.overlay {
  background-color: #004d26;
  color: white;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.overlay-content {
  padding: 40px;
}

.overlay h1 {
  font-size: clamp(2rem, 4vw, 3rem); /* Responsive font that won't overflow */
  font-weight: 800;
  margin-bottom: 10px;
}

.ghost-btn {
  margin-top: 20px;
  padding: 12px 40px;
  background: #d1d1d1;
  color: #004d26;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
}

.ghost-btn:hover {
  background: #b1b1b1;
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
  transform: translateY(-5px);
  transition: transform 0.3s, box-shadow 0.3s;
}

/* Tablet/Mobile Fix */
@media (max-width: 768px) {
  .auth-card {
    flex-direction: column;
    height: auto;
  }
  .overlay-container {
    position: relative;
    left: 0;
    width: 100%;
    height: 250px;
    transform: none !important;
  }
  .forms-bg-container {
    flex-direction: column;
  }
}
</style>