<template>
  <vue-final-modal
    v-slot="{ params, close }"
    v-bind="$attrs"
    classes="modal-container"
    content-class="modal-content"
    v-on="$listeners"
  >
    <span class="modal__title">
      <slot name="title"></slot>
    </span>
    <div class="modal__content">
      <slot v-bind:params="params"></slot>
    </div>
    <div class="modal__action">
      <!-- <v-button @click="$emit('confirm', close)">confirm</v-button>
            <v-button @click="$emit('cancel', close)">cancel</v-button> -->
    </div>
    <div class="modal__close">
      <slot name="modal-close-text"></slot>
    </div>
  </vue-final-modal>
</template>

<script>
import { $vfm, VueFinalModal, ModalsContainer } from "vue-final-modal";

export default {
  //   name: 'CustomModal',
  components: {
    VueFinalModal,
  },

  inheritAttrs: false,
};
</script>

<style scoped>
::v-deep .modal-container {
  display: flex;
  justify-content: center;
  align-items: center;
  max-height: 70%;
  max-width: 50%;
}
::v-deep .modal-content {
  position: relative;
  display: flex;
  flex-direction: column;
  max-height: 90%;
  margin: 0 1rem;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
  background: #fff;
}
.modal__title {
  margin: 0 2rem 0 0;
  font-size: 1.5rem;
  font-weight: 700;
}
.modal__content {
  flex-grow: 1;
  overflow-y: auto;
}
.modal__action {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-shrink: 0;
  padding: 1rem 0 0;
}
.modal__close {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
}
</style>

<style scoped>
.dark-mode div::v-deep .modal-content {
  border-color: #2d3748;
  background-color: #1a202c;
}
</style>
