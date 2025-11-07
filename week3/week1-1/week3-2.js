// ==============================
// 抓取資料、合併、顯示
// ==============================
window.addEventListener("load", async () => {
    const url1 = "https://cwpeng.github.io/test/assignment-3-1";
    const url2 = "https://cwpeng.github.io/test/assignment-3-2";

    const [res1, res2] = await Promise.all([fetch(url1), fetch(url2)]);

    const json1 = await res1.json();
    const json2 = await res2.json();

    const data1 = json1.rows;
    const data2 = json2.rows;
    const host = json2.host;

    const map1 = {};
    data1.forEach(item => {
        map1[item.serial] = item;
    });

    const attractions = data2.map(item => {
        const paired = map1[item.serial];

        // 檢查破圖
        if(!paired) {
            console.warn(`Serial ${item.serial} 沒有對應到的資料`);
            return null; 
        }

        const prefix = "/d_upload_ttn/sceneadmin/pic/";
        const parts = item.pics.split(prefix);
        const firstPic = prefix + (parts[1] || "");
        const fullUrl = host + firstPic

        return{
            name: paired.sname,
            image: fullUrl
        };
    }).filter(item => item !== null); //過濾掉 null

    renderList(attractions.slice(0,3));
    renderBlocks(attractions.slice(3,13));
});


// 利用函式將list設為資料陣列, container設為要把景點放進去的html元素 //
function renderList(list) {
    const container = document.getElementById("bar-section");

    const barClasses = ["full", "twth", "oth"]

    list.forEach((item, index) => {
        const bar = document.createElement("div");
        bar.className = `bar ${barClasses[index]}`;

        const img = document.createElement("img");
        img.src = item.image;

        const text = document.createElement("div");
        text.className = "bar-text"
        text.textContent = item.name;

        bar.appendChild(img);
        bar.appendChild(text);
        container.appendChild(bar);
    });
}   

function renderBlocks(list) {
    const container = document.getElementById("content-section");

    list.forEach(item => {
        const block = document.createElement("div");
        block.className = "block";

        const img = document.createElement("img");
        img.src = item.image;

        const star = document.createElement("img");
        star.className = "star-img";
        star.src = "star.png";

        const overlay = document.createElement("div");
        overlay.className = "overlay";

        const text = document.createElement("span");
        text.textContent = item.name;

        overlay.appendChild(text);
        block.appendChild(img);
        block.appendChild(star);
        block.appendChild(overlay);

        container.appendChild(block);

    });
}


// ==============================
// 執行
// ==============================


