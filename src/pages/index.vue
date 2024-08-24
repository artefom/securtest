<template>
  <div class="bgimage">
    <div class="front-shrooms" />

    <div class="logoline logoline-size">
      <a href="https://t.me/gribni_tsa">
        <div style="display: flex; flex-direction: row; align-items: center">
          <h1>грибни:ца</h1>
          <img
            class="logo-image"
            src="/design/logo_white.svg"
            alt="Description"
          />
        </div>
      </a>
    </div>

    <div v-if="showQuestions" class="questionarie-container">
      <div style="display: flex; align-items: center; margin-bottom: 0.5em">
        <img
          class="title-image"
          src="/design/logo_white.svg"
          alt="Description"
        />
        <div>
          <h1 class="qtitle">
            опросник <br />
            по безопасности
          </h1>
        </div>
      </div>

      <div class="default-border questionarie-body">
        <div
          v-if="showLanding"
          style="display: flex; flex-direction: column; height: 100%"
        >
          <p class="question-body" style="flex-grow: 1">
            Привет! Этот тест — часть
            <a href="http://localhost:8080">хендбука</a> , в котором мы собрали
            инструкции по организации и проведению некоторых оффлайн-ивентов.
            Если вы попали сюда из другого места и не читали этот документ,
            обязательно с ним ознакомьтесь, это поможет корректному восприятию
            теста!
          </p>

          <div style="width: 100%; display: flex; justify-content: center">
            <v-btn
              style="
                font-family: 'Kelly Slab', sans-serif;
                font-weight: bold;
                color: white !important;
              "
              size="x-large"
              color="primary"
              variant="flat"
              @click="start"
              >Пройти опросник</v-btn
            >
          </div>
        </div>

        <v-carousel
          v-if="!showLanding"
          :continuous="false"
          :show-arrows="false"
          progress="primary"
          hide-delimiters
          hide-delimiter-background
          v-model="currentSlide"
          style="height: 100%; overflow: hidden"
        >
          <v-carousel-item v-for="(question, i) in questions" :key="i">
            <div
              style="
                height: 100%;
                overflow: hidden;
                display: flex;
                flex-direction: column;
              "
            >
              <div style="flex-grow: 1; overflow-y: auto">
                <p class="question-body">{{ question.question }}</p>
              </div>

              <div style="display: flex; align-items: center">
                <v-btn
                  prepend-icon="mdi-check"
                  :variant="
                    question.answer_display === true ? 'flat' : 'outlined'
                  "
                  text="Да"
                  color="primary"
                  density="comfortable"
                  size="large"
                  @click="select(i, true)"
                ></v-btn>

                <v-btn
                  prepend-icon="mdi-close"
                  :variant="
                    question.answer_display === false ? 'flat' : 'outlined'
                  "
                  class="ml-3"
                  text="Нет"
                  density="comfortable"
                  size="large"
                  @click="select(i, false)"
                ></v-btn>

                <div style="flex-grow: 1"></div>
                <v-btn
                  v-if="i > 0"
                  class="back-button"
                  icon="mdi-arrow-left"
                  variant="outlined"
                  density="comfortable"
                  @click="back"
                />
              </div>
            </div>
          </v-carousel-item>
        </v-carousel>
      </div>
    </div>
    <v-expand-transition>
      <div
        v-if="!showQuestions"
        style="
          height: 100%;
          width: 100%;
          display: flex;
          justify-content: center;
          background-image: url('/design/desktop_white_bg.svg');
          background-size: cover;
          background-position: center;
          background-repeat: no-repeat;
        "
      >
        <div class="results-body" style="">
          <div class="logoline-results logoline-size">
            <a href="https://t.me/gribni_tsa">
              <div
                style="display: flex; flex-direction: row; align-items: center"
              >
                <h1>грибни:ца</h1>
                <img
                  class="logo-image"
                  src="/design/logo_dark.svg"
                  alt="Description"
                />
              </div>
            </a>
          </div>

          <h1 class="results-header">результаты</h1>

          <div class="results-scroller">
            <div class="test-result" v-html="testResult" />

            <div class="disclaimer">
              Если у вас остались вопросы по безопасности или организации,
              вы хотите запустить какой-то движ, но вам не хватает поддержки —
              напишите в наш
              <a href="https://t.me/gribnitsa1_bot"> анонимный бот </a>
              и мы постараемся вам помочь! У наших активист:ок есть возможность
              провести с желающими индивидуальные анонимные созвоны для разбора
              конкретно вашего кейса.
            </div>

            <div
              style="
                width: 100%;
                display: flex;
                justify-content: center;
                margin-top: 3em;
                margin-bottom: 7em;
              "
            >
              <v-btn variant="text" @click="reset">Пройти тест заново</v-btn>
            </div>
          </div>
        </div>
      </div>
    </v-expand-transition>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

let currentSlide = ref(0);
let showLanding = ref(true);
let showQuestions = ref(true);
let testResult = null;

let questions = [
  {
    question: "Вы приглашаете только знакомых людей?",
    answer: null,
    answer_display: null,
  },
  {
    question:
      "Даете ли вы объявление о вашем мероприятии публично: со \
      своего личного аккаунта в открытых источниках?",
    answer: null,
    answer_display: null,
  },
  {
    question:
      "Есть ли у вас в каком-либо виде база с личными данными участни:ц?",
    answer: null,
    answer_display: null,
  },
  {
    question:
      "Есть ли в названии мероприятия триггерная лексика\
      (например “ЛГБТ-шабаш” или “антивоенный пикник”)?",
    answer: null,
    answer_display: null,
  },
  {
    question:
      "Были ли уже случаи задержаний\\арестов на подобных мероприятиях,\
       даже если формально они законные (был случай, когда работников \
       гей-бара привлекли за ЛГБТ-пропаганду)?",
    answer: null,
    answer_display: null,
  },
  {
    question:
      "Является ли сама тематика мероприятия потенциально триггерной \
      и привлекающей внимание полиции (квир-активизм, феминизм, \
      антивоенный активизм итп), или же вы собрались делать \
      что-то безобидное (пикник, воркшоп по вязанию крючком, \
      просмотр нового диснеевского мультика)?",
    answer: null,
    answer_display: null,
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

function start() {
  showLanding.value = false;
}

async function showResult() {
  await fetchRenderedText();
  showQuestions.value = false;
}

function select(i, answer) {
  questions[i].answer = answer;

  setTimeout(() => {
    questions[i].answer_display = answer;
  }, 100);

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
.logoline-size {
  font-size: 0.8em;
}

.logoline a {
  color: white;
}

.logoline-results a {
  color: rgb(var(--v-theme-background));
}

.logoline {
  position: absolute;
  width: 90%;
  max-width: 60rem;
  display: flex;
  justify-content: right;
  margin-top: 1em;
}

.logoline-results {
  width: 100%;
  display: flex;
  justify-content: right;
  color: rgb(var(--v-theme-background));
}

.front-shrooms {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  pointer-events: none;
  background-image: url("/design/desktop_shrooms.svg");
  z-index: 2;
}

.disclaimer {
  margin-top: 1em;
  background-color: rgb(var(--v-theme-background));
  color: white;
  border-radius: 1em;
  padding: 1em;
}

.question-body a {
  color: rgb(var(--v-theme-primary));
  font-weight: bold;
}

.disclaimer a {
  color: rgb(var(--v-theme-primary));
  font-weight: bold;
}

.bgimage {
  height: 100%;
  max-height: 100vh;
  max-width: 100vw;
  width: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-image: url("/design/desktop_background.svg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
}

/* Styles for portrait-oriented screens (more height than width) */
@media (max-aspect-ratio: 3/4) {
  .logoline {
    margin-top: 3em;
  }

  .bgimage {
    justify-content: baseline !important;
  }
  .questionarie-container {
    margin-top: 3.5em;
    height: 65%;
  }
  .front-shrooms {
    background-image: url("/design/mobile_shrooms.svg");
  }
  .bgimage {
    background-image: url("/design/mobile_background.svg");
  }
}

@media (min-aspect-ratio: 3/4) {
  .questionarie-container {
    margin-top: 15vh;
    height: 70%;
  }
}

.questionarie-container {
  width: 90%;
  max-width: 60rem;
  display: flex;
  flex-direction: column;
}

.questionarie-body {
  width: 100%;
  height: 100%;
  padding: 3em 5em;
  border-radius: 1em;
}
.question-body {
  font-size: 1.5em;
  margin-bottom: 1em;
  margin-top: 1em;
}

.logo-image {
  height: 3em;
  display: block;
  margin-left: 5px;
}

.title-image {
  height: 6em;
  width: auto;
  display: block;
  margin-right: 16px;
}

.results-body {
  width: 100%;
  max-width: 50em;
  padding: 2em;
  color: black;
  display: flex;
  flex-direction: column;
  background-color: white;
  z-index: 3;
}

.results-header {
  margin-bottom: 1em;
  color: rgb(var(--v-theme-background));
  font-size: 3em;
}

.results-scroller {
  overflow-y: auto;
  padding-right: 3em;
}

.back-button {
  margin-right: calc(
    max(
      -1 * ((50vw + (max(50vw, 50vh * 1.77777) * 0.55) - 20px) -
            (50vw + (min(90vw, 60rem) / 2))),
      0px
    )
  );
}

/* For extra-large screens */
@media (min-width: 120em) {
  .disclaimer {
    font-size: 1.4em;
  }

  .questionarie-body {
    max-height: 30rem;
  }

  .results-body {
    max-width: 80em;
  }
}

@media (max-width: 700px) {
  .results-body {
    padding: 2em 0.5em;
  }

  .results-scroller {
    padding-right: 1em;
  }
}

@media (max-width: 600px) or (max-height: 500px) or ((max-height: 900px) and (max-width: 700px)) {
  .logoline-size {
    font-size: 0.5em;
  }

  .title-image {
    height: 3em;
  }

  .results-header {
    font-size: 2em;
  }

  .question-body {
    font-size: 1.2em;
  }

  .questionarie-body {
    padding: 2em;
  }

  .qtitle {
    font-size: 1.5em;
  }
}
@media (max-width: 350px) {
  .back-button {
    display: none;
  }
}
@media (max-width: 300px) or ((max-height: 500px) and (max-width: 700px)) or ((max-height: 400px) and (max-width: 900px)) or ((max-height: 700px) and (max-width: 400px)) {
  .logoline-size {
    font-size: 0.3em;
  }

  .results-header {
    font-size: 1em;
  }

  .title-image {
    height: 2em;
  }

  .qtitle {
    font-size: 1em;
  }

  .question-body {
    font-size: 1em;
  }

  .questionarie-body {
    padding: 1em;
  }
}
</style>

<style>
@media (max-width: 600px) {
  .test-result {
    font-size: 0.8em !important;
  }

  .v-btn--size-large {
    padding: 0px !important;
  }
}
@media (max-width: 300px) {
  .test-result {
    font-size: 0.5em !important;
  }

  .v-btn--size-large {
    min-width: 50px !important;
  }
  .v-btn__prepend {
    margin-inline: 0 !important;
  }
  .questionarie-body .v-btn__content {
    display: none !important;
  }
}

.test-result p {
  font-size: 1.4em;
}

.test-result span {
  color: rgb(var(--v-theme-secondary));
  font-weight: bold;
}

.test-result a {
  color: rgb(var(--v-theme-primary));
  font-weight: bold;
}

.test-result ul {
  padding: 0em 0em 1em 1em;
}

.test-result ul li {
  padding-top: 0.5em;
  font-size: 1.4em;
}

.test-result p {
  margin-top: 10px;
}
</style>
