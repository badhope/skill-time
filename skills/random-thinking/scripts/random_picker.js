import crypto from 'crypto';

function rollDice(sides) {
    return crypto.randomInt(1, sides + 1);
}

function pareto(alpha = 1.5, xm = 1) {
    const u = crypto.randomInt(1, 1000000) / 1000000;
    return Math.round(xm * Math.pow(u, -1/alpha));
}

function levyStable(alpha = 1.0, gamma = 1.0) {
    const phi = (crypto.randomInt(1, 1000000) / 1000000 - 0.5) * Math.PI;
    const w = -Math.log(crypto.randomInt(1, 1000000) / 1000000);
    const left = Math.sin(alpha * phi) / Math.pow(Math.cos(phi), 1/alpha);
    const right = Math.pow(Math.cos(phi * (1-alpha)) / w, (1-alpha)/alpha);
    return Math.round(gamma * left * right);
}

function semanticJumpDistance() {
    return Math.abs(levyStable(1.0, 2.0));
}

function wanderSteps() {
    const steps = pareto(1.5, 2);
    return Math.min(Math.max(steps, 1), 15);
}

function dynamicNoiseLevel(step, totalSteps) {
    const phase = (step / totalSteps) * Math.PI;
    const base = 0.15;
    const oscillation = 0.1 * Math.sin(2 * phase);
    const criticalPoint = step === Math.floor(totalSteps/2) ? 0.2 : 0;
    return base + oscillation + criticalPoint;
}

function generateAllSeedsV2() {
    const stepCount = wanderSteps();
    
    const result = {
        version: "2.0",
        path_seed: rollDice(4),
        format_seed: rollDice(4),
        failure_seed: rollDice(100),
        lane_change_seed: rollDice(20),
        collapse_seed: rollDice(100),
        wander_steps: wanderSteps(),
        semantic_jump: semanticJumpDistance(),
        initial_noise: dynamicNoiseLevel(0, stepCount),
        dmn_activation: crypto.randomInt(30, 70) / 100,
        ecn_activation: crypto.randomInt(30, 70) / 100,
        timestamp: new Date().toISOString()
    };
    
    console.log('=== RANDOM-SKILL v2.0 SEED RESULT ===');
    console.log(JSON.stringify(result, null, 2));
    console.log('====================================');
    
    const pathNames = ['Creative Divergence', 'Analytical Deconstruction', 
                       'Mind-Wandering', 'Pure Random Surprise'];
    const formatNames = ['Clean Structured', 'Casual Chat Style', 
                         'Works-in-Progress', 'Digression First'];
    
    console.log(`\n📊 NEURODYNAMICS:`);
    console.log(`  Path: ${result.path_seed} → ${pathNames[result.path_seed - 1]}`);
    console.log(`  Format: ${result.format_seed} → ${formatNames[result.format_seed - 1]}`);
    console.log(`  Wander Steps: ${result.wander_steps} (Pareto α=1.5, 90% ≤ 4 steps)`);
    console.log(`  Semantic Jump: ${result.semantic_jump} (Levy α=1.0)`);
    console.log(`  Initial Noise: ${(result.initial_noise*100).toFixed(0)}%`);
    console.log(`  DMN: ${(result.dmn_activation*100).toFixed(0)}% ↔ ECN: ${(result.ecn_activation*100).toFixed(0)}%`);
    
    console.log(`\n💥 SPECIAL EVENTS:`);
    console.log(`  Minor Failure: ${result.failure_seed <= 30 ? 'YES (30%)' : 'NO'}`);
    console.log(`  Lane Change: ${result.lane_change_seed <= 2 ? 'YES (10%)' : 'NO'}`);
    console.log(`  ⚠️  Framework Collapse: ${result.collapse_seed <= 5 ? 'YES (5%)' : 'NO'}`);
    
    console.log(`\n✅ THESE VALUES ARE FINAL. NO TAKE-BACKS.`);
    
    return result;
}

const args = process.argv.slice(2);

if (args.includes('v2') || args.includes('all')) {
    generateAllSeedsV2();
} else if (args[0] === 'dice') {
    const sides = parseInt(args[1]) || 4;
    console.log(`D${sides}: ${rollDice(sides)}`);
} else if (args[0] === 'wander') {
    console.log(`Wander steps: ${wanderSteps()}`);
    console.log(`(Pareto α=1.5, most are 1-4, rare 10+)`);
} else if (args[0] === 'jump') {
    console.log(`Semantic jump distance: ${semanticJumpDistance()}`);
    console.log(`(Levy α=1.0, most are 1-3, rare big jumps)`);
} else if (args[0] === 'test') {
    console.log('Running 100 distribution tests...\n');
    const dist = {};
    for (let i=0; i<100; i++) {
        const s = wanderSteps();
        dist[s] = (dist[s] || 0) + 1;
    }
    console.log('Wander step distribution (Pareto α=1.5):');
    Object.keys(dist).sort((a,b)=>a-b).forEach(k => {
        console.log(`  ${k} steps: ${dist[k]} times`);
    });
} else {
    console.log('Usage:');
    console.log('  node random_picker.js v2           - v2.0 full neurodynamics seed');
    console.log('  node random_picker.js wander       - Sample Pareto wander steps');
    console.log('  node random_picker.js jump         - Sample Levy semantic jumps');
    console.log('  node random_picker.js test         - Run 100 distribution tests');
    console.log('  node random_picker.js dice 20      - Roll a D20');
}

export {
    rollDice,
    pareto,
    levyStable,
    wanderSteps,
    semanticJumpDistance,
    dynamicNoiseLevel,
    generateAllSeedsV2
};
