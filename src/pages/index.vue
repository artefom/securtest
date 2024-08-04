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
        <div class="test-result" v-html="testResult" />
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
import axios from "axios";

let currentSlide = ref(0);
let showQuestions = ref(true);
let testResult = null;

let questions = [
  {
    question: "Вы приглашаете только знакомых людей?",
    answer: null,
  },
  {
    question:
      "Даете ли вы объявление о вашем мероприятии публично со\
      своего личного аккаунта или от своего имени?",
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
  {
    question:
      "Были ли уже случаи задержаний\\арестов на подобных мероприятиях,\
       даже если формально они законные (был случай, когда работников \
       гей-бара привлекли за ЛГБТ-пропаганду)?",
    answer: null,
  },
  {
    question:
      "Является ли сама тематика мероприятия потенциально\
      триггерной и привлекающей внимание полиции\
      (ЛГБТ-повестка, феминизм, антивоенный активизм итп),\
      или же вы собрались делать что-то безобидное\
      (пикник, просмотр нового диснеевского мультика)?",
    answer: null,
  },
];

function encodeAnswers(questions) {
  // Ensure there are exactly 6 questions
  if (questions.length !== 6) {
    throw new Error("There must be exactly 6 questions");
  }

  // Convert boolean answers to binary string
  let binaryString = questions.map((q) => (q.answer ? "1" : "0")).join("");

  return binaryString;
}

async function fetchRenderedText() {
  console.log("Fetching result");
  try {
    const variantNum = encodeAnswers(questions);
    const response = await axios.get(`/rendered/variant${variantNum}`);
    testResult = response.data;
  } catch (error) {
    console.error("Error fetching rendered text:", error);
  }
}

function back() {
  if (currentSlide.value > 0) {
    currentSlide.value -= 1;
  }
}

async function showResult() {
  await fetchRenderedText();
  showQuestions.value = false;
}

function select(i, answer) {
  questions[i].answer = answer;

  if (currentSlide.value < questions.length - 1) {
    currentSlide.value += 1;
  } else {
    showResult();
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

<style>
.test-result span {
  color: #1956b3;
  font-weight: bold;
}

.test-result p {
  margin-top: 10px;
}
</style>
