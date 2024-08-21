const select = document.querySelector("#converter-type");
const unitA = document.querySelector("#unit-a");
const unitB = document.querySelector("#unit-b");
const inputA = document.querySelector("#a")
const inputB = document.querySelector("#b")

const data = {
    time : {
        units : ["hours", "min", "seconds", "ms"],
        ratios : [1, 60, 60*60, 60*60*1000]
    },
    pressure : {
        units : ["atm", "Pa", "bar", "mPa"],
        ratios : [1, 101325, 1.01, 0.1]
    },
    length : {
        units : ["cm", "m", "km", "mile"],
        ratios : [1, 0.01, 0.00001, 0.0000062]
    },
    mass : {
        units : ["mg", "g", "kg", "t"],
        ratios : [1, 0.001, 0.000001, 1**(0.10**9)]
    },
    info : {
        units : ["gb", "mb", "kb", "b"],
        ratios : [1, 2**10, 2**20, 2**30]
    },
    volume : {
        units : ["l", "km", "chark", "shkaliki"],
        ratios : [1, 0.001, 8.13, 16.26]
    },
}

select.addEventListener("input", (event) => {
    console.log(event);
    const type = event.target.value;
    unitA.innerHTML = data[type].units.map((unit, i) => `<option value="${data[type].ratios[i]}">${unit}</option>`);
    unitB.innerHTML = data[type].units.map((unit, i) => `<option value="${data[type].ratios[i]}">${unit}</option>`)
})
inputA.addEventListener("input", (event) => {
    const a = event.target.value;
    const ratioA = Number(unitA.value);
    const ratioB = Number(unitB.value);
    let mid = ratioB / ratioA;
    let result = mid * a;
    inputB.value = result
})
inputB.addEventListener("input", (event) => {
    const b = event.target.value;
    const ratioA = Number(unitA.value);
    const ratioB = Number(unitB.value);
    let mid = ratioA / ratioB;
    let result = mid * b;
    inputA.value = result
})



const text = document.querySelector("#texth2");
const colorSwitch = document.querySelector("#colorSwitch");

colorSwitch.addEventListener("input", (event) => {
    const a = event.target.value;
    text.style.color = a;
    console.log(a);
});
const h1 = document.querySelector("h1");
console.log(getComputedStyle(h1).color);


const task = document.querySelector("#inputTask");
const add = document.querySelector("#addTask");
add.addEventListener("click", (e) => {
    task.value

})

const get_files = async (dir) => {
    let files = await eel.get_files(dir)();
    files = JSON.parse(files);
    if (files.error) return false;
    console.log("Получены файлы", files);
    return files
}

const get_files2 = (dir) => {
    return new Promise((resolve, reject) => {
        eel.get_files(dir)().then((files) => {
            files = JSON.parse(files);
            if (files.error) reject(false);
            resolve(files);
        }).catch(err => reject(err))
    })
}

// get_files2("C:/Users/Gleb77/Downloads/Telegram Desktop").then(files => console.log(files))