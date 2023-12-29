import { showAlert } from "./alert.js"
const validityMap = new Map()

// collectValue: (name: string): string | string[] | undefined
// collectValue takes the name of the input field and returns the text value of that field for input[type=text],
// or the selected value for input[type=radio], or the array of all the selected values for input[type=checkbox]
export const collectValue = (name) => {
  const textInput = document.querySelector(`#${name} input[type=text]`)
  if (textInput !== null) {
    return textInput.value
  }

  const checkboxes = document.querySelectorAll(`#${name} input[type=checkbox]`)
  if (checkboxes.length !== 0) {
    return (
      Array.from(checkboxes)
        .filter((box) => box.checked)
        .map((box) => box.value)
    )
  }

  const radios = document.querySelectorAll(`#${name} input[type=radio]`)
  if (radios.length !== 0) {
    return Array.from(radios).find((radio) => radio.checked)?.value ?? ""
  }

  console.warn(
    `there's no supported input element in #${name}. Did you mistype the element ID?`,
  )
  return undefined
}

const setInvalid = (name, message) => {
  const inputGroup = document.querySelector(`#${name}`)
  inputGroup.classList.add("invalid")

  inputGroup.querySelector(".error-text").innerText = message
}

const unsetInvalid = (name) =>
  document.querySelector(`#${name}`).classList.remove("invalid")

const checkIfValid = async (name, ...validators) => {
  const value = collectValue(name)
  let errFlag = false
  for (const validator of validators) {
    try {
      await validator(value, name)
    } catch (err) {
      errFlag = true
      setInvalid(name, err.message)
      break
    }
  }
  !errFlag && unsetInvalid(name)

  return !errFlag
}

export const init = () => {
  document.querySelectorAll(".option-group > label").forEach((label) => {
    label.addEventListener("mouseenter", () => {
      label.control.classList.add("hover")
    })
    label.addEventListener("mouseleave", () => {
      label.control.classList.remove("hover")
    })
  })

  document.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault()
    const submit = e.currentTarget.querySelector("button")

    // run all the validators concurrently and finally check that all of them returned true
    const isValid = (await Promise.all(
      [...validityMap.entries()].map(([name, validators]) =>
        checkIfValid(name, ...validators)
      ),
    )).reduce((valid, cur) => valid && cur, true)

    if (!isValid) {
      return
    }

    submit.disabled = true
    submit.innerText = "Submitting..."

    const fields = Array.from(e.currentTarget.querySelectorAll("input")).map(
      (it) => it.name,
    ).filter(it => it !== "form-name")

    const fd = fields.map((name) => [name, collectValue(name)]).reduce(
      (fd, [name, value]) => {
        fd.set(name, value)
        return fd
      },
      new FormData(),
    )
    
    // netlify expects the form name
    fd.set("form-name", document.querySelector("input[name=form-name]").value)
    
    // netlify will pick the request up and store its value in the forms backend
    const res = await fetch("/", {
      body: fd,
      method: "POST"
    })
    
    const newLine = (innerWidth <= 580) ? "\n" : " "
    const result = (res.status === 200)
      ? `Your form was submitted successfully.${newLine}You will be contacted shortly`
      : `Your form submission failed.${newLine}Try again later`
    
    showAlert(result)
  })
}

export const validateOn = (...revalidateOn) => (name, ...validators) => {
  if (validityMap.has(name)) {
    throw new Error(`Validator: re-adding validtors for ${name}`)
  }
  validityMap.set(name, validators)
  const input = document.querySelector(`#${name} input[type=text]`)
  input?.addEventListener(
    "blur",
    async () => await checkIfValid(name, ...validators),
  )

  // bad code, but something to get us started
  revalidateOn.map((event) => {
    document.querySelectorAll(`#${name} input`).forEach((input) => {
      input.addEventListener(
        event,
        async () => await checkIfValid(name, ...validators),
      )
    })
  })
}

export const required = (message) => (value) => {
  if (value.length === 0) {
    throw new Error(message)
  }
}