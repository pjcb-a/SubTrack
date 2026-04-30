<script setup>
import { ref } from 'vue';
import LoginForm from './LoginForm.vue';
import RegisterForm from './RegisterForm.vue';

const isLogin = ref(true);
</script>

<template>
  <div class="auth-shell">
    <div class="auth-card" :class="{ 'is-register-active': !isLogin }">
      <div class="forms-bg-container">
        <div class="form-section register-section">
          <RegisterForm />
        </div>
        <div class="form-section login-section">
          <LoginForm />
        </div>
      </div>

      <div class="overlay-container">
        <div class="overlay">
          <div class="brand-mark">SUBTRACK</div>
          <div class="overlay-copy">
            <span class="eyebrow">{{ isLogin ? 'Built to manage' : 'Get started' }}</span>
            <h1>{{ isLogin ? 'Recurring Payments, Clearly Seen.' : 'Build Your Own Subscription Space.' }}</h1>
            <p>
              {{
                isLogin
                  ? 'Track renewals, control spending caps, and keep your subscription history organized in one clean system.'
                  : 'Register once and start with a clean account that reflects only your own real subscription data.'
              }}
            </p>
          </div>

          <div class="overlay-actions">
            <p>{{ isLogin ? 'Need an account?' : 'Already have an account?' }}</p>
            <button type="button" class="ghost-btn" @click="isLogin = !isLogin">
              {{ isLogin ? 'Create account' : 'Sign in' }}
            </button>
          </div>

          <p class="overlay-footer">
            {{
              isLogin
                ? 'One workspace for renewals, spending limits, and account control.'
                : 'Switch back to sign in once your account is ready.'
            }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-shell {
  min-height: 100vh;
  width: 100%;
  background: #f3f5f1;
}

.auth-card {
  position: relative;
  width: 100%;
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr 1fr;
  overflow: hidden;
}

.forms-bg-container {
  display: contents;
}

.form-section {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 64px 72px;
  background:
    radial-gradient(circle at top left, rgba(13, 106, 69, 0.06), transparent 28%),
    linear-gradient(180deg, #f7f8f5 0%, #f0f4ef 100%);
}

.overlay-container {
  position: absolute;
  inset: 0 auto 0 0;
  width: 50%;
  height: 100%;
  z-index: 10;
  transition: transform 0.6s ease-in-out;
}

.is-register-active .overlay-container {
  transform: translateX(100%);
}

.overlay {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 56px 56px 60px;
  color: #f7fbf8;
  background:
    radial-gradient(circle at 82% 14%, rgba(133, 205, 170, 0.18), transparent 18%),
    radial-gradient(circle at 72% 70%, rgba(255, 255, 255, 0.08), transparent 24%),
    linear-gradient(180deg, #004d26 0%, #0a5f35 52%, #0d6a45 100%);
}

.brand-mark {
  font-size: 0.92rem;
  font-weight: 800;
  letter-spacing: 0.36em;
}

.overlay-copy {
  display: grid;
  gap: 20px;
  max-width: 470px;
}

.eyebrow {
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: rgba(242, 249, 244, 0.72);
}

.overlay h1 {
  font-size: clamp(3.2rem, 5vw, 5rem);
  line-height: 0.96;
  font-weight: 800;
  letter-spacing: -0.04em;
}

.overlay-copy p,
.overlay-actions p,
.overlay-footer {
  font-size: 1rem;
  line-height: 1.72;
  color: rgba(244, 249, 245, 0.84);
}

.overlay-actions {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
}

.ghost-btn {
  border: 1px solid rgba(255, 255, 255, 0.22);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.14);
  color: #ffffff;
  padding: 12px 20px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.2s ease, background 0.2s ease, border-color 0.2s ease;
}

.ghost-btn:hover {
  transform: translateY(-1px);
  background: rgba(255, 255, 255, 0.22);
  border-color: rgba(255, 255, 255, 0.34);
}

.overlay-footer {
  color: rgba(244, 249, 245, 0.66);
}

@media (max-width: 960px) {
  .auth-card {
    grid-template-columns: 1fr;
  }

  .forms-bg-container {
    display: flex;
    flex-direction: column;
  }

  .form-section {
    min-height: auto;
    padding: 32px 18px 36px;
  }

  .overlay-container {
    position: relative;
    width: 100%;
    transform: none !important;
    order: -1;
  }

  .overlay {
    min-height: 380px;
    padding: 30px 24px 32px;
  }

  .overlay h1 {
    font-size: clamp(2.5rem, 11vw, 4rem);
  }
}
</style>
