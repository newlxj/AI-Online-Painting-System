<!-- https://github.com/newlxj/sdweb-multi-user-website for newlxj -->
<template>
  <el-row>
    <el-col>
      <el-divider content-position="center">
        <el-switch v-model="theme" inline-prompt :active-icon="Moon" :inactive-icon="Sunny"
          style="margin-left: 10px;--el-switch-on-color: #ff0000; --el-switch-off-color: #409eff"
          @change="toggleDark()" />
      </el-divider>

    </el-col>
  </el-row>
</template>
<script setup lang="ts">
import { ref, watch } from "vue";
import { Moon, Sunny } from "@element-plus/icons-vue";
import { useDark, useToggle, useStorage } from "@vueuse/core";
const isDark = ref(useDark());
const toggleDark = useToggle(isDark);
// 切换按钮 localStorage 中的值，保证刷新不重置
const vueuseColorScheme = useStorage("vueuse-color-scheme", null);
const theme = vueuseColorScheme.value === "auto" ? ref(false) : ref(true);
// watch(
//   theme,
//   (newVal, oldVal) => {
//     console.log(newVal);
//     if (newVal) {
//       window.document.documentElement.setAttribute("data-theme", "light");
//     } else {
//       window.document.documentElement.setAttribute("data-theme", "dark");
//     }
//   },
//   {
//     immediate: true,
//   }
// );
</script>