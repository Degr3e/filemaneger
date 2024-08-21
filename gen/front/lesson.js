// let a = 4;
// let b = 5.4;
// let c = "asdf";
// let d = true;


// let age = Number(prompt('введите свой возраст'))
// if (age >= 14) {
//     alert("проходи!")
// }
// else {
//     alert('Увы но ты не проходишь(')
// }

// let first = Number(prompt("баллы за первый"));
// let second = Number(prompt("баллы за первый"));

// if ((first + second >= 150) || (first >=70 && second >= 70)) {
//     alert("Урааа вы прошли")
// }
// else {
//     alert('Ооо нет как грустно( ')
// }

// let numbers = [5, 5, 7, 56, 123]

// for (let i = numbers.length - 1; i >= 0; i--) {
//     alert(numbers[i])
// }

// let a = document.querySelector('#a')
// let b = document.querySelector('#b')
// let go = document.querySelector('#go')
// let result = document.querySelector('#result')


// go.addEventListener('click', () => {
//     result.textContent = Number(a.value) + Number(b.value);
// })


// const h1 = document.querySelector("h1");
// h1.innerHTML = "<ul><li>hello</li></

// let numbers = [12, 2, 45, 5645, 213]
// numbers = numbers.map((number) => number**2)
// console.log(numbers)


// let words = ["dog", "phone", "hello", "print", "alert"]
// words = words.map((word) => "<li>" + word + "</li>")
// console.log(words)


// let numbers = [12, 2, 45, 5645, 213]
// numbers = numbers.filter((num) => num % 2 === 0)
// console.log(numbers)

// let words = ["dog", "phone", "hello", "print", "alert", "hi", "cat"]
// words = words.filter((word) => word.length < 5)
// console.log(words)


let numbers = [12, 2, 45, 5645, 213]
numbers = numbers.sort((a,b) => a - b)
console.log(numbers)
