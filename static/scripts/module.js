import { init, validateOn, required } from "./forms.js"
init()

const validate = validateOn("change", "keyup")

const requiredFields = ["name", "gender", "morality", "languages"]
requiredFields.map(data => validate(data, required(`${data.charAt(0).toUpperCase() + data.slice(1)} is required`)))

// validate("age", required("Age is required"), async value => {
//   if (Number.isNaN(Number(value))) {
//     throw new Error("Age should be a number")
//   }
// })

validate("mobile", required("Phone No. is required"), async value => {
  if (Number.isNaN(Number(value))) {
    throw new Error("Mobile should contain number")
  }
})

validate("email", async value => {
  const mailformat = /^[A-Za-z\d\.]+\@[A-Za-z]+\.[a-z]{2,3}$/
  if (!mailformat.test(value)) {
    throw new Error("Please enter a valid email")
  }
})

// validate("github", required("Github User Profile Link is required"), async value => {
//   const githubformat = /^[a-zA-Z0-9_-]+$/
//   if (!githubformat.test(value)) {
//     throw new Error("Please enter a valid address.")
//   }
// })