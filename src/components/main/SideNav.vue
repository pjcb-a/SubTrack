<script setup>

</script>

<!-- Left side nav bar -->

<template>
    <div class="side-nav">
        <div class="profile">
            <img src="../subtrack/src/assets/hero.png" alt="Profile Picture" class="profile-pic">
            <h4 class="username">Welcome, {{ name }}</h4>
        </div>

        <nav class="nav-links"> 
            <div class="nav-home"></div>
            <div class="nav-subscriptions"></div>
            <div class="nav-history"></div>
            <div class="nav-about"></div>
        </nav>

        <div class="logout"><i class="fa-solid fa-arrow-right-from-bracket"></i></div>
    </div> 
</template>

<style scoped>
.side-nav {
    position: fixed;
    width: 250px;
    height: 100vh;
    background-color: #1e5628; /* Dark background */
    color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 30px;
    border-radius: 12px;
}

.logout {
    width: 50px;
    height: 50px;
    margin: auto 0;
    background-color: #e0e0e0;
    border-radius: 15px;
    color: #1e5628;
}

.logout i {
    padding: 12px;
    font-size: 1.5rem;
}
</style>