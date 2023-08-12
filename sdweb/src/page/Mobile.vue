
<!-- https://github.com/newlxj/stablediffusion-website-online for newlxj -->
<script setup>
import Theme from '../components/Theme.vue'
import Album from '../components/Album.vue'
import DialogShowImage from '../components/DialogShowImage.vue'
</script>

<template>
    <Theme />
    <Album />
    <DialogShowImage />
</template>
<style scoped>
.logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
    filter: drop-shadow(0 0 2em #42b883aa);
}

html.dark {
    /* custom dark bg color */
    --el-bg-color: #626aef;
}
</style>
