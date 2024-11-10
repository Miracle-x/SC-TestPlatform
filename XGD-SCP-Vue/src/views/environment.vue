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
console.log()
export default {
  computed: {
    iframeUrl(){
      return  'https://localhost:8443/#/overview?namespace=net1' // 你想要嵌入的网页URL
    }
  },

};
</script>