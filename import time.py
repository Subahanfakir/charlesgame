<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Charles River Tycoon</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --sky-top: #0f2027;
            --sky-bot: #203a43;
            --water-clean: rgba(41, 128, 185, 0.85);
            --water-dirty: rgba(62, 39, 35, 0.9);
            --ui-bg: rgba(20, 20, 30, 0.9);
            --accent: #f39c12;
            --green: #27ae60;
            --red: #c0392b;
        }

        * { box-sizing: border-box; user-select: none; cursor: default; font-family: 'Segoe UI', sans-serif; }

        body {
            margin: 0; overflow: hidden; height: 100vh; width: 100vw;
            background: linear-gradient(to bottom, var(--sky-top), var(--sky-bot));
            color: white;
        }

        /* --- SCENERY (BACKGROUND) --- */
        .world {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            display: flex; flex-direction: column; justify-content: flex-end;
            pointer-events: none; /* Allow clicking through to game elements if needed */
        }

        /* Boston Skyline */
        .skyline {
            height: 300px; width: 100%;
            position: absolute; bottom: 35%; left: 0;
            display: flex; align-items: flex-end; justify-content: center;
            gap: 2px; z-index: 1;
            opacity: 0.8;
        }

        .building { background: #1a1a2e; border: 1px solid #000; position: relative; }
        .window-grid { 
            width: 100%; height: 100%; 
            background-image: radial-gradient(#f1c40f 15%, transparent 16%);
            background-size: 10px 10px; opacity: 0.3;
        }

        /* Specific Landmarks */
        .pru { width: 60px; height: 220px; background: #2c3e50; border-top: 3px solid #95a5a6; }
        .hancock { width: 50px; height: 260px; background: #34495e; transform: skewY(-5deg); opacity: 0.9; box-shadow: inset 5px 0 10px rgba(0,0,0,0.5); }
        .citgo-sign {
            width: 50px; height: 50px; background: white; margin-bottom: 10px; margin-left: 30px;
            display: flex; justify-content: center; align-items: center; position: relative;
        }
        .citgo-tri { 
            width: 0; height: 0; border-left: 15px solid transparent; border-right: 15px solid transparent; border-bottom: 25px solid #c0392b; 
            animation: pulse 2s infinite;
        }
        @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }

        /* The Esplanade (Green Bank) */
        .esplanade {
            position: absolute; bottom: 30%; left: 0; width: 100%; height: 60px;
            background: #27ae60; border-top: 4px solid #1e8449;
            z-index: 2;
            display: flex; align-items: flex-end; justify-content: space-around;
        }
        .tree { font-size: 1.5rem; color: #145a32; margin-bottom: 5px; }
        .runner { font-size: 0.8rem; color: #ecf0f1; animation: run 10s linear infinite; position: absolute; bottom: 10px; }
        @keyframes run { 0% { left: -5%; } 100% { left: 105%; } }

        /* --- THE RIVER (FOREGROUND) --- */
        .river-container {
            position: absolute; bottom: 0; left: 0; width: 100%; height: 35%;
            background: var(--water-clean);
            backdrop-filter: blur(4px);
            border-top: 4px solid rgba(255,255,255,0.2);
            z-index: 10; /* In front of city */
            transition: background 1s;
            overflow: hidden;
            pointer-events: auto; /* Interactive */
            cursor: crosshair;
        }

        .wave {
            position: absolute; top: 0; left: 0; width: 200%; height: 100%;
            background: repeating-linear-gradient(
                45deg,
                rgba(255,255,255,0.05) 0px,
                rgba(255,255,255,0.05) 10px,
                transparent 10px,
                transparent 50px
            );
            animation: flow 20s linear infinite;
        }
        @keyframes flow { from { transform: translateX(0); } to { transform: translateX(-50%); } }

        /* Interactive Items */
        .trash-item {
            position: absolute; font-size: 1.8rem; color: #bdc3c7;
            cursor: pointer; transition: transform 0.1s;
            animation: bob 2s ease-in-out infinite;
            filter: drop-shadow(0 3px 3px rgba(0,0,0,0.5));
        }
        .trash-item:hover { transform: scale(1.2); color: white; }
        .trash-item:active { transform: scale(0.9); }

        .duck {
            position: absolute; font-size: 1.5rem; color: #f1c40f;
            transition: left 10s linear; pointer-events: none;
            z-index: 5;
        }

        .boat {
            position: absolute; font-size: 3rem; color: #ecf0f1;
            bottom: 50%; z-index: 4; animation: sail 15s linear infinite;
            opacity: 0.8;
        }
        @keyframes sail { from { left: -20%; } to { left: 120%; } }

        @keyframes bob { 0%,100% { margin-top: 0; } 50% { margin-top: -10px; } }

        /* --- UI (HUD) --- */
        .ui-panel {
            position: absolute; z-index: 100; pointer-events: none;
            width: 100%; padding: 15px;
            display: flex; justify-content: space-between;
        }

        .stats-bar {
            background: var(--ui-bg); padding: 10px 20px; border-radius: 30px;
            display: flex; gap: 20px; align-items: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            pointer-events: auto;
        }

        .stat { display: flex; flex-direction: column; align-items: center; min-width: 60px; }
        .stat-label { font-size: 0.7rem; text-transform: uppercase; opacity: 0.7; }
        .stat-val { font-size: 1.2rem; font-weight: bold; font-family: monospace; }
        .money { color: #f1c40f; }

        /* Bottom Controls */
        .control-deck {
            position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
            display: flex; gap: 15px; z-index: 100;
            background: var(--ui-bg); padding: 15px; border-radius: 15px;
            pointer-events: auto;
        }

        .upgrade-card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            width: 120px; padding: 10px; border-radius: 8px;
            text-align: center; cursor: pointer;
            transition: all 0.2s; position: relative;
        }
        .upgrade-card:hover { background: rgba(255,255,255,0.15); transform: translateY(-5px); }
        .upgrade-card:active { transform: scale(0.95); }
        .upgrade-card.disabled { opacity: 0.4; cursor: not-allowed; filter: grayscale(1); }

        .card-icon { font-size: 1.5rem; margin-bottom: 5px; color: var(--accent); }
        .card-title { font-size: 0.8rem; font-weight: bold; }
        .card-cost { font-size: 0.75rem; color: #f1c40f; margin-top: 4px; }
        .card-lvl { position: absolute; top: 2px; right: 5px; font-size: 0.7rem; background: #333; padding: 2px 5px; border-radius: 4px; }

        /* Floating Text */
        .float-txt {
            position: absolute; font-weight: bold; font-size: 1.2rem; pointer-events: none;
            animation: floatUp 1s ease-out forwards; text-shadow: 0 2px 4px black; z-index: 200;
        }
        @keyframes floatUp { 0% { transform: translateY(0) scale(1); opacity: 1; } 100% { transform: translateY(-50px) scale(1.5); opacity: 0; } }

        /* Intro/Outro */
        .modal {
            position: fixed; inset: 0; background: rgba(0,0,0,0.95); z-index: 1000;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            text-align: center; pointer-events: auto;
        }
        .hidden { display: none; }
        .big-btn {
            padding: 15px 50px; font-size: 1.5rem; background: var(--green); border: none; 
            color: white; border-radius: 50px; cursor: pointer; margin-top: 30px;
            animation: pulseBtn 2s infinite;
        }
        @keyframes pulseBtn { 0% { box-shadow: 0 0 0 0 rgba(39, 174, 96, 0.7); } 70% { box-shadow: 0 0 0 20px rgba(39, 174, 96, 0); } 100% { box-shadow: 0 0 0 0 rgba(39, 174, 96, 0); } }

    </style>
</head>
<body>

    <!-- --- WORLD LAYER --- -->
    <div class="world">
        <div class="skyline">
            <div class="building" style="width: 40px; height: 100px;"></div>
            <div class="building" style="width: 50px; height: 150px;"><div class="window-grid"></div></div>
            <div class="pru"><div class="window-grid"></div></div>
            <div class="building" style="width: 30px; height: 80px;"></div>
            <div class="hancock"></div>
            <div class="citgo-sign"><div class="citgo-tri"></div></div>
            <div class="building" style="width: 60px; height: 120px;"><div class="window-grid"></div></div>
        </div>
        <div class="esplanade">
            <i class="fa-solid fa-tree tree"></i>
            <i class="fa-solid fa-tree tree" style="font-size: 1.2rem"></i>
            <i class="fa-solid fa-person-running runner"></i>
            <i class="fa-solid fa-tree tree"></i>
            <i class="fa-solid fa-tree tree" style="font-size: 1.8rem"></i>
        </div>
    </div>

    <!-- --- INTERACTIVE RIVER --- -->
    <div class="river-container" id="river" onclick="handleRiverClick(event)">
        <div class="wave"></div>
        <!-- Boats/Trash spawn here -->
        <div id="riverItems"></div>
    </div>

    <!-- --- HUD --- -->
    <div class="ui-panel">
        <div class="stats-bar">
            <div class="stat">
                <span class="stat-label">Budget</span>
                <span class="stat-val money" id="uiMoney">$0</span>
            </div>
            <div style="width: 1px; height: 30px; background: #444;"></div>
            <div class="stat">
                <span class="stat-label">Purity</span>
                <span class="stat-val" id="uiPurity">100%</span>
            </div>
            <div class="stat">
                <span class="stat-label">Eco-Life</span>
                <span class="stat-val" id="uiEco">100%</span>
            </div>
        </div>
        
        <div class="stats-bar">
            <i class="fa-solid fa-clock" style="opacity: 0.5"></i>
            <span id="timeDisplay">Day 1</span>
        </div>
    </div>

    <!-- --- UPGRADES --- -->
    <div class="control-deck">
        <div class="upgrade-card" id="upg-volunteer" onclick="buyUpgrade('volunteer')">
            <div class="card-lvl" id="lvl-volunteer">0</div>
            <i class="fa-solid fa-users card-icon"></i>
            <div class="card-title">Student Volunteers</div>
            <div class="card-cost" id="cost-volunteer">$50</div>
        </div>

        <div class="upgrade-card" id="upg-filter" onclick="buyUpgrade('filter')">
            <div class="card-lvl" id="lvl-filter">0</div>
            <i class="fa-solid fa-filter-circle-xmark card-icon"></i>
            <div class="card-title">Water Filter</div>
            <div class="card-cost" id="cost-filter">$150</div>
        </div>

        <div class="upgrade-card" id="upg-duck" onclick="buyUpgrade('duck')">
            <div class="card-lvl" id="lvl-duck">0</div>
            <i class="fa-solid fa-bus card-icon"></i>
            <div class="card-title">Duck Tour Ad</div>
            <div class="card-cost" id="cost-duck">$300</div>
        </div>
    </div>

    <!-- --- MODALS --- -->
    <div class="modal" id="startModal">
        <h1 style="font-size: 3rem; color: var(--accent); margin-bottom: 0;">Charles River Tycoon</h1>
        <p style="color: #aaa; margin-top: 5px;">Clean the river. Build the economy. Save the skyline.</p>
        
        <div style="margin: 30px; text-align: left; background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
            <p><i class="fa-solid fa-hand-pointer" style="color: var(--accent)"></i> <strong>CLICK TRASH</strong> to clean & earn cash.</p>
            <p><i class="fa-solid fa-arrow-trend-up" style="color: var(--green)"></i> <strong>BUY UPGRADES</strong> to automate cleaning.</p>
            <p><i class="fa-solid fa-skull-crossbones" style="color: var(--red)"></i> Don't let Purity hit 0%!</p>
        </div>

        <button class="big-btn" onclick="startGame()">Open the River</button>
    </div>

    <div class="modal hidden" id="loseModal">
        <h1 style="color: var(--red)">RIVER CLOSED</h1>
        <p>The EPA shut you down due to toxic sludge.</p>
        <h2 id="finalDays">Days Survived: 0</h2>
        <button class="big-btn" onclick="location.reload()">Try Again</button>
    </div>

<script>
    /* --- GAME STATE --- */
    const STATE = {
        money: 0,
        purity: 50, // Starts halfway
        eco: 50,
        day: 1,
        running: false,
        tickSpeed: 1000,
        pollutionRate: 1,
        incomeRate: 0,
        trashSpawnRate: 0.4 // Chance per tick
    };

    const UPGRADES = {
        volunteer: { name: "Volunteers", cost: 50, count: 0, effect: "Auto-click trash slowly" },
        filter: { name: "Filter", cost: 150, count: 0, effect: "+1 Purity/tick" },
        duck: { name: "Duck Tour", cost: 300, count: 0, effect: "+$5 Income/tick" }
    };

    /* --- DOM REFERENCES --- */
    const ui = {
        money: document.getElementById('uiMoney'),
        purity: document.getElementById('uiPurity'),
        eco: document.getElementById('uiEco'),
        time: document.getElementById('timeDisplay'),
        river: document.getElementById('riverItems'),
        riverBg: document.getElementById('river'),
        btns: {
            volunteer: document.getElementById('upg-volunteer'),
            filter: document.getElementById('upg-filter'),
            duck: document.getElementById('upg-duck')
        }
    };

    /* --- CORE ENGINE --- */
    function startGame() {
        document.getElementById('startModal').classList.add('hidden');
        STATE.running = true;
        STATE.money = 20; // Starter cash
        updateUI();
        
        // Start loops
        setInterval(gameTick, STATE.tickSpeed);
        setInterval(spawnTrashLoop, 1500);
        setInterval(spawnAmbientLoop, 4000);
    }

    function gameTick() {
        if(!STATE.running) return;

        STATE.day++;
        
        // 1. Passive Pollution vs Filters
        let purityChange = -STATE.pollutionRate;
        purityChange += (UPGRADES.filter.count * 0.5); // Filters help
        changePurity(purityChange);

        // 2. Passive Income
        let income = UPGRADES.duck.count * 5;
        if(STATE.purity > 80) income += 10; // Clean river bonus
        if(STATE.eco > 80) income += 5;
        addMoney(income);

        // 3. Passive Eco Change
        if(STATE.purity > 60) STATE.eco = Math.min(100, STATE.eco + 1);
        else STATE.eco = Math.max(0, STATE.eco - 1);

        // Difficulty Ramp
        if(STATE.day % 20 === 0) STATE.pollutionRate += 0.2;

        updateUI();
        checkGameOver();
        updateButtonStates();
    }

    /* --- INTERACTION --- */
    function handleRiverClick(e) {
        // If clicked strictly on water (not trash), splash effect
        if(e.target.id === 'river' || e.target.id === 'riverItems') {
            createFloatText("Splash!", e.clientX, e.clientY, "#87CEEB");
        }
    }

    function clickTrash(e, element) {
        e.stopPropagation(); // Don't trigger river click
        
        // Remove element
        element.remove();
        
        // Reward
        const reward = 10 + (UPGRADES.duck.count * 2);
        addMoney(reward);
        changePurity(2); // Manual cleaning helps purity
        
        // Feedback
        createFloatText(`+$${reward}`, e.clientX, e.clientY, "#f1c40f");
        createFloatText("+Clean", e.clientX, e.clientY - 30, "#2ecc71");
    }

    function buyUpgrade(type) {
        const upg = UPGRADES[type];
        if(STATE.money >= upg.cost) {
            addMoney(-upg.cost);
            upg.count++;
            upg.cost = Math.floor(upg.cost * 1.5); // Price scaling
            
            // Update DOM card
            document.getElementById(`lvl-${type}`).innerText = upg.count;
            document.getElementById(`cost-${type}`).innerText = `$${upg.cost}`;
            
            createFloatText("Upgraded!", window.innerWidth/2, window.innerHeight - 100, "#fff");
            updateButtonStates();
            
            // Visual effect for upgrades
            if(type === 'duck') spawnBoat();
        }
    }

    /* --- SPAWNING SYSTEMS --- */
    function spawnTrashLoop() {
        if(!STATE.running) return;
        // Base chance + difficulty
        if(Math.random() > 0.3) {
            const icons = ['fa-bottle-water', 'fa-pizza-slice', 'fa-newspaper', 'fa-can-food', 'fa-box'];
            const icon = icons[Math.floor(Math.random() * icons.length)];
            
            const el = document.createElement('i');
            el.className = `fa-solid ${icon} trash-item`;
            // Random Position in river area
            el.style.left = (10 + Math.random() * 80) + '%';
            el.style.bottom = (10 + Math.random() * 70) + '%';
            // Random Rotation
            el.style.transform = `rotate(${Math.random()*360}deg)`;
            
            el.onclick = (e) => clickTrash(e, el);
            
            ui.river.appendChild(el);

            // Trash hurts purity immediately on spawn slightly? 
            // Or just existence? Let's make existing trash hurt stats in tick?
            // For simplicity, trash is just potential money.
        }
        
        // Auto-clean by volunteers
        if(UPGRADES.volunteer.count > 0) {
            const trash = document.querySelectorAll('.trash-item');
            if(trash.length > 0) {
                // Volunteers clean 1 item per level per few seconds logic?
                // Let's just randomly remove one based on level
                if(Math.random() < (UPGRADES.volunteer.count * 0.2)) {
                   const t = trash[0];
                   const rect = t.getBoundingClientRect();
                   createFloatText("Volunteer!", rect.left, rect.top, "#fff");
                   t.remove();
                   addMoney(5); // Volunteers generate less money
                   changePurity(1);
                }
            }
        }
    }

    function spawnAmbientLoop() {
        if(!STATE.running) return;
        // Spawn Fish or Ducks based on Eco
        if(STATE.eco > 40 && Math.random() > 0.6) {
            const duck = document.createElement('i');
            duck.className = "fa-solid fa-fish duck"; // reusing class for movement
            duck.style.color = "#a2d9ce";
            duck.style.bottom = (Math.random() * 80) + '%';
            duck.style.left = "-10%";
            duck.style.transition = "left 15s linear";
            ui.river.appendChild(duck);
            
            setTimeout(() => duck.style.left = "110%", 50);
            setTimeout(() => duck.remove(), 16000);
        }
    }

    function spawnBoat() {
        const boat = document.createElement('i');
        boat.className = "fa-solid fa-ferry boat";
        ui.river.appendChild(boat);
        // CSS animation handles movement
        setTimeout(() => boat.remove(), 15000);
    }

    /* --- UTILITIES --- */
    function addMoney(amount) {
        STATE.money += amount;
        // Pulse animation on money
        ui.money.style.transform = "scale(1.2)";
        setTimeout(() => ui.money.style.transform = "scale(1)", 100);
    }

    function changePurity(amount) {
        STATE.purity = Math.max(0, Math.min(100, STATE.purity + amount));
        
        // Visual Water Murkiness
        const dirtyR = 62, dirtyG = 39, dirtyB = 35;
        const cleanR = 41, cleanG = 128, cleanB = 185;
        const ratio = STATE.purity / 100;
        
        const r = Math.round(dirtyR + ratio * (cleanR - dirtyR));
        const g = Math.round(dirtyG + ratio * (cleanG - dirtyG));
        const b = Math.round(dirtyB + ratio * (cleanB - dirtyB));
        
        ui.riverBg.style.background = `rgba(${r}, ${g}, ${b}, 0.85)`;
    }

    function updateUI() {
        ui.money.innerText = `$${STATE.money}`;
        ui.purity.innerText = `${Math.floor(STATE.purity)}%`;
        ui.eco.innerText = `${Math.floor(STATE.eco)}%`;
        ui.time.innerText = `Day ${STATE.day}`;
        
        ui.purity.style.color = STATE.purity < 30 ? '#c0392b' : '#fff';
    }

    function updateButtonStates() {
        Object.keys(UPGRADES).forEach(key => {
            const btn = ui.btns[key];
            if(STATE.money < UPGRADES[key].cost) {
                btn.classList.add('disabled');
            } else {
                btn.classList.remove('disabled');
            }
        });
    }

    function createFloatText(text, x, y, color) {
        const el = document.createElement('div');
        el.className = 'float-txt';
        el.innerText = text;
        el.style.color = color;
        el.style.left = x + 'px';
        el.style.top = y + 'px';
        document.body.appendChild(el);
        setTimeout(() => el.remove(), 1000);
    }

    function checkGameOver() {
        if(STATE.purity <= 0) {
            STATE.running = false;
            document.getElementById('finalDays').innerText = `Days Survived: ${STATE.day}`;
            document.getElementById('loseModal').classList.remove('hidden');
        }
    }

</script>
</body>
</html>