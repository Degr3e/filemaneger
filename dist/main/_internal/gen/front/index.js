// Получение файлов по пути
const get_files = async (dir) => {
    let files = await eel.get_files(dir)();
    files = JSON.parse(files);
    if (files.error) return false;
    console.log("Получены файлы", files);
    return files
}
const getFullPath = (folderName) => {
    const oldWay = ways.textContent;
    console.log("Попытка получить файлы по пути", oldWay + folderName);
    if (oldWay.indexOf(":") >= 0 && oldWay.length <= 3){ // Если C:/
        return oldWay + folderName;
    }
    else{
        return oldWay + "/" + folderName;      
    }
}
// Добавление обработчиков на папки (при нажатии переходим)
const addFolderListeners = () => document.querySelectorAll(".folder").forEach(folder => folder.addEventListener("click", () => {
    const folderName = folder.querySelector(".folder-name").textContent.trim();
    openFolder(getFullPath(folderName))
}))
// Получение частей пути по полному пути
const getPathParts = (path) => (path.indexOf("/") !== -1) ? path.split("/") : path.split("\\");
// Отрисовка пути по частям пути
const renderWay = (pathParts) => pathParts.forEach((part, i) => {
    if (part != ""){
        const span = document.createElement("span");
        span.textContent = part + "/";
        span.className = "way-part";
        const fullPath = pathParts.slice(0, i + 1).join("/");
        span.addEventListener("click", () => openFolder(fullPath));
        ways.appendChild(span); 
    }
})
// Открытие папки
const openFolder = (dir) => {
    console.log("Открытие папки", dir);
    ways.innerHTML = "";
    if(dir.indexOf(":") > 0 && dir.length < 3) dir = `${dir}/`;
    get_files(dir).then((data) => {
        if (!data){
            directoryInput.style.background = "red";
        }
        else{
            files = data
            renderFiles(files)
            addFolderListeners();
            renderWay(getPathParts(dir));
            createChart(files);
        }
    })
}
// Отрисовка файлов
const renderFiles = (files) => fileList.querySelector("tbody").innerHTML = files.map(file =>{
    // Конвертер размеров
    const translateSize = (size) => {
        let times = 0
        const quantity = ["b", "kb", "mb", "gb", "tb"]
        while (size / 1024 > 1){
            times ++;
            size = size / 1024
        }
        return Math.round(size) + quantity[times] 
    }

    const date = new Date(file.details.created * 1000);
    const addZero = (n) => (n < 10) ? `0${n}` : n;
    const strDate = `${addZero(date.getDate())}.${addZero(date.getMonth() + 1)}.${date.getFullYear()} ${addZero(date.getHours())}:${addZero(date.getMinutes())}:${addZero(date.getSeconds())}`
    if (file.basic.is_dir){
        return `<tr class="folder">
            <td class = "folder-name">${folderIcon}  ${file.basic.name}</td>
            <td>${strDate}</td>
            <td>Папка с файлами</td>
            <td>${translateSize(file.details.size)}</td>
        </tr>`
    }
    else{
        let parts = file.basic.name.split(".")
        let type = parts[parts.length-1]
        let name = parts.slice(0, parts.length-1).join(".")
        return `<tr>
            <td>${fileIcon}  ${name}</td>
            <td>${strDate}</td>
            <td>${type}</td>
            <td>${translateSize(file.details.size)}</td>
        </tr>`
    }
}).join("\n");
// Сортировка файлов
const size = document.querySelector("#size");
const sortFiles = (files, sort) => {
    switch(sort){
        case "size_asc": return files.sort((a,b) => b.details.size - a.details.size);
        case "size_desc": return files.sort((a,b) => a.details.size - b.details.size);
        case "name_asc": return files.sort((a,b) => (a.basic.name < b.basic.name ) ? -1 : 1);
        case "name_desc": return files.sort((a,b) => (b.basic.name < a.basic.name ) ? -1 : 1);
        case "date_asc": return files.sort((a,b) => b.details.modified - a.details.modified);
        case "date_desc": return files.sort((a,b) => a.details.modified - b.details.modified);
        default: return files
        
    }
}
// Сортировка файлов по размеру
size.addEventListener("click", (e) => {
    if (lastSort != "size_asc"){
        files = sortFiles(files, "size_asc")
        renderFiles(files)
        lastSort = "size_asc"
        // size.innerHTML = "Размер" + sizeIcon
    }
    else if (lastSort != "size_desc"){
        files = sortFiles(files, "size_desc")
        renderFiles(files)
        lastSort = "size_desc"
    }
})
    // Сортировка файлов по имени
const fileName = document.querySelector("#fileName")
fileName.addEventListener("click", (e) => {
    console.log("sort")
    if (lastSort != "name_asc"){
        files = sortFiles(files, "name_asc")
        renderFiles(files)
        lastSort = "name_asc"
    }
    else if (lastSort != "name_desc"){
        files = sortFiles(files, "name_desc")
        renderFiles(files)
        lastSort = "name_desc"
    }
})

const fileDate = document.querySelector("#fileDate");

fileDate.addEventListener("click", (e) => {
    console.log("sort")
    if (lastSort != "date_asc"){
        files = sortFiles(files, "date_asc")
        renderFiles(files)
        lastSort = "date_asc"
    }
    else if (lastSort != "date_desc"){
        files = sortFiles(files, "date_desc")
        renderFiles(files)
        lastSort = "date_desc"
    }
})
let lastSort;
let files = [];
let chart;
const sizeIcon = `<img src = "down-arrow.png">`
const folderIcon = `<img src = "open-folder.png">`
const fileIcon = `<img src = "document.png">`

const ways = document.querySelector(".ways");
const directoryInput = document.querySelector("#directory");
const btn = document.querySelector("#btn");
const fileList = document.querySelector(".files");

btn.addEventListener("click", () => {
    const dir = directoryInput.value;
    openFolder(dir); 
})

const sort = document.querySelector("#sort")
// Создаем дату для графика
const fileFormats = (files) => {
    let data = []
    
    for (let i = 0; i < files.length ;  i++){
        if(!files[i].basic.is_dir){
            let parts = files[i].basic.name.split(".");
            let format = parts[parts.length-1];
            let size = files[i].details.size;
            let obj = data.find(row => row.format === format);
            if (obj){
                data = data.filter(row => row.format != format)
                obj.size += size
                data.push(obj)
            }
            else{
                data.push({format, size})
            }
        }
        else{
            // Получение файлов из вложенных папок (в процессе)

            // get_files(getFullPath(files[i].basic.name)).then(filesInFolder => {
            //     console.log("Файлы в вложенной папке", getFullPath(files[i].basic.name));
            //     console.log(filesInFolder);
            // })
        }
    }
    return data
}
function createChart (files) {
    const canvasElement = document.getElementById('Chart');
    const data = fileFormats(files);
    if(chart) chart.destroy();
    chart = new Chart(
      canvasElement,
      {
        type: 'doughnut',
        data: {
          labels: data.map(row => row.format),
          datasets: [
            {
              label: 'Занимает места: ',
              data: data.map(row => row.size)
            }
          ]
        }
      }
    );
  };



