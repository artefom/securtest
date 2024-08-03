<template>
  <div
    style="
      display: flex;
      flex-direction: column;
      height: 100%;
      justify-content: center;
      align-items: center;
      padding: 1em;
    "
  >
    <h1 class="mb-10">Опросник по безопасности</h1>

    <v-expand-transition>
      <div v-if="showQuestions" style="max-width: 700px; width: 100%">
        <v-carousel
          :continuous="false"
          :show-arrows="false"
          progress="#1956b3"
          height="400"
          hide-delimiters
          hide-delimiter-background
          v-model="currentSlide"
        >
          <v-carousel-item v-for="(question, i) in questions" :key="i">
            <div style="height: 100%; display: flex; flex-direction: column">
              <div style="flex-grow: 1; display: flex; align-items: center">
                <p class="question-body">{{ question.question }}</p>
              </div>

              <div style="display: flex; align-items: center">
                <v-btn
                  prepend-icon="mdi-check"
                  :variant="question.answer === true ? 'flat' : 'outlined'"
                  text="Да"
                  color="#1956b3"
                  @click="select(i, true)"
                ></v-btn>

                <v-btn
                  prepend-icon="mdi-close"
                  :variant="question.answer === false ? 'flat' : 'outlined'"
                  class="ml-3"
                  text="Нет"
                  color="black"
                  @click="select(i, false)"
                ></v-btn>

                <div style="flex-grow: 1"></div>
                <v-btn
                  v-if="i > 0"
                  icon="mdi-arrow-left"
                  variant="text"
                  @click="back"
                />
              </div>
            </div>
          </v-carousel-item>
        </v-carousel>
      </div>
    </v-expand-transition>

    <v-expand-transition>
      <div
        v-if="!showQuestions"
        style="
          max-width: 700px;
          display: flex;
          flex-direction: column;
          justify-items: center;
        "
      >
        <p>
          Lorem ipsum odor amet, consectetuer adipiscing elit. Dictum adipiscing
          lobortis platea montes mus nascetur, nisi eget senectus. Maecenas
          montes per nulla sociosqu, elementum conubia sit potenti. Torquent
          fusce sagittis maecenas purus porttitor aenean montes sociosqu.
          Pharetra vivamus ac proin purus mus amet tempor netus. Rhoncus
          elementum velit blandit et magna quis luctus nibh. Neque donec semper
          pellentesque auctor rutrum. Gravida luctus habitasse, bibendum
          elementum felis consequat sit rhoncus. Commodo congue nisl quis
          lacinia dis aptent aliquam justo. Rutrum himenaeos viverra ex nec quam
          mattis nascetur fames. Maximus nibh sem parturient pellentesque sed
          luctus. Orci finibus magnis ridiculus proin lacinia justo est
          scelerisque. Cursus scelerisque conubia aliquam; in dui bibendum.
          Adipiscing ullamcorper finibus vulputate vulputate eleifend gravida
          condimentum. Parturient auctor mi senectus, tellus habitant tempor
          aenean. Tristique curabitur nisi nisl ac viverra adipiscing. Euismod
          dictum posuere porta sapien sed curae id hendrerit.
        </p>
        <v-btn variant="text" class="mt-5" @click="reset"
          >Пройти тест заново</v-btn
        >
      </div>
    </v-expand-transition>

    <!-- <v-card class="mx-auto" prepend-icon="$vuetify" :subtitle="`Вопрос ${question_number} из 10`" width="400">
      <template v-slot:title>
        <span class="font-weight-black">Мой очень сложный тест</span>
      </template>

<v-card-text class="pt-4">
  Даете ли вы объявление о вашем мероприятии открыто (в открытых
  тг-каналах, в объявлениях, со своего личного аккаунта)?
</v-card-text>

<template v-slot:actions>
        <v-btn text="Да" color="success" @click="question_number++"></v-btn>
        <v-btn text="Нет" color="error"></v-btn>
      </template>
</v-card> -->
  </div>
</template>

<script setup>
import { ref } from "vue";

let currentSlide = ref(0);
let showQuestions = ref(true);

let questions = [
  {
    question:
      "Даете ли вы объявление о вашем мероприятии открыто\
      (в открытых тг-каналах, в объявлениях, \
      со своего личного аккаунта)?",
    answer: null,
  },
  {
    question: "Вы приглашаете только знакомых людей?",
    answer: null,
  },
  {
    question:
      "Есть ли у вас в каком-либо виде база с данными участников ваших мероприятий?\
      (включая чаты в мессенджерах и группы в соцсетях)",
    answer: null,
  },
  {
    question:
      "Есть ли в названии мероприятия триггерная лексика\
      (например “ЛГБТ-шабаш” или “антивоенный пикник”)?",
    answer: null,
  },
];

function back() {
  if (currentSlide.value > 0) {
    currentSlide.value -= 1;
  }
}

function select(i, answer) {
  console.log("Selecting");
  questions[i].answer = answer;

  if (currentSlide.value < questions.length - 1) {
    currentSlide.value += 1;
  } else {
    showQuestions.value = false;
  }
}

function reset() {
  for (let question of questions) {
    question.answer = null;
  }

  currentSlide.value = 0;
  showQuestions.value = true;
}
</script>

<style scoped>
.question-body {
  font-size: 1.5em;
}
</style>
