<template>
  <iframe
      :src="iframeUrl"
      width="100%"
      height="100%"
      frameborder="0"
      allowfullscreen
      loading="lazy"
  ></iframe>
</template>

<script>
export default {
  data() {
    return {
      iframeUrl: 'https://localhost:8834/', // 你想要嵌入的网页URL
    };
  },
};
</script>