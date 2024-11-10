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
      iframeUrl: 'http://172.18.0.2:31800/d/Application_K8s_Pod_Map/application-k8s-pod-map?orgId=1&var-datasource=DeepFlow&var-cluster=__any&var-namespace=net1&var-workload=__any&var-protocol=__disabled', // 你想要嵌入的网页URL
    };
  },
};
</script>


