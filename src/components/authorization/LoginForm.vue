<script setup>
</script>

<template>
    <!-- Login -->
    <div class="form-content">
    <h1>Login</h1>
    <div class="input-group">
        <label for="name">Username</label>
        <input type="text" id="name" placeholder="Enter username"/>
    </div>
    
    <div class="input-group">
        <label for="password">Password</label>
        <input type="password" id="password" placeholder="Enter password" />
    </div>

    <button class="submit-btn">Login</button>
  </div>
</template>

<style scoped>
    .form-content {
  width: 100%;
  max-width: 340px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-content h1 {
  font-family: 'Montserrat', sans-serif;
  font-weight: 800;
  /* Reduced size so it stays inside the white area */
  font-size: clamp(3rem, 4vw, 3.2rem); 
  margin-bottom: 4rem; 
  letter-spacing: 1.5px;
  text-align: center;
  color: #1e5628;
}

.input-group {
  width: 100%;
  margin-bottom: 10px;
  text-align: left;
  padding: 2px;
}

.input-group label {
  display: block;
  padding-left: 5px;
  font-size: 0.9rem;
  font-weight: 700;
  color: #666;
}

.input-group input {
  width: 100%;
  padding: 10px;
  background: #e0e0e0;
  border: 1px solid transparent;
  border-radius: 10px;
  font-family: 'Montserrat', sans-serif;
  transition: border-color 0.5s ease;
}

.input-group input:focus {
  outline: none;
  border-color: #1e5628;
  background: #fff;
}

.submit-btn {
  width: 100%; 
  max-width: 220px; 
  align-self: center; 
  padding: 10px;
  background-color: #1e5628;
  color: #fff;
  border-radius: 12px;
  font-size: 1.2rem; 
  font-weight: 500;
  letter-spacing: 1px;
  margin-top: 20px;
}

.submit-btn:hover {
  background: #2e813d;
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
  transform: translateY(-5px);
  transition: transform 0.3s, box-shadow 0.3s;
}
</style>
