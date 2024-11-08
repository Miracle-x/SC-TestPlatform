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
      iframeUrl: 'http://172.18.0.3:30429/d/Application_K8s_Pod_Map/application-k8s-pod-map?orgId=1&from=1731002942978&to=1731003842978', // 你想要嵌入的网页URL
    };
  },
};
</script>


