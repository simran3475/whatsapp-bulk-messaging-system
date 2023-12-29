export const showAlert = (value) => {
	document.body.classList.add("alert")
	const pre = document.body.querySelector("#overlay pre")
	
	// lord forgive me for using innerHTML, but im too bored
	// FIXME: don't use innerHTML here
	// FIXME: this span shouldn't be set in js, but if you use .innerText the span will be removed from the html. find a better way of doing this.
	pre.innerHTML =
window.alert(
  <span id="alert">"${value}"</span>
);<span id="blink"></span>
}