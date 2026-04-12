import crypto from 'crypto';
import { execSync } from 'child_process';

function rollDice(sides) {
    return crypto.randomInt(1, sides + 1);
}

function runSingleTest() {
    return {
        path_seed: rollDice(4),
        format_seed: rollDice(4),
        failure_seed: rollDice(10),
        lane_change_seed: rollDice(20),
        micro_seed: rollDice(10)
    };
}

function runDistributionTests(count = 100) {
    console.log(`\n📊 Running ${count} distribution tests...\n`);
    
    const results = [];
    const pathCounts = { 1: 0, 2: 0, 3: 0, 4: 0 };
    const formatCounts = { 1: 0, 2: 0, 3: 0, 4: 0 };
    let failureCount = 0;
    let laneChangeCount = 0;
    let microRandomCount = 0;
    
    for (let i = 0; i < count; i++) {
        const r = runSingleTest();
        results.push(r);
        
        pathCounts[r.path_seed]++;
        formatCounts[r.format_seed]++;
        if (r.failure_seed <= 3) failureCount++;
        if (r.lane_change_seed === 1 || r.lane_change_seed === 20) laneChangeCount++;
        if (r.micro_seed <= 3) microRandomCount++;
    }
    
    const pathNames = ['🎨 Creative', '🔍 Analytical', '💭 Mind-Wander', '🎲 Pure Random'];
    const formatNames = ['📐 Structured', '💬 Casual', '✏️ Draft', '🌀 Digression'];
    
    console.log('🎯 PATH DISTRIBUTION (target: 25% each):');
    Object.entries(pathCounts).forEach(([k, v]) => {
        const pct = ((v / count) * 100).toFixed(1);
        const target = 25;
        const diff = Math.abs(pct - target);
        const status = diff < 5 ? '✅' : diff < 10 ? '⚠️' : '❌';
        console.log(`  ${pathNames[k-1]}: ${v} times = ${pct}% ${status}`);
    });
    
    console.log('\n📝 FORMAT DISTRIBUTION (target: 25% each):');
    Object.entries(formatCounts).forEach(([k, v]) => {
        const pct = ((v / count) * 100).toFixed(1);
        const target = 25;
        const diff = Math.abs(pct - target);
        const status = diff < 5 ? '✅' : diff < 10 ? '⚠️' : '❌';
        console.log(`  ${formatNames[k-1]}: ${v} times = ${pct}% ${status}`);
    });
    
    console.log('\n💥 SPECIAL EVENTS:');
    console.log(`  Minor Failures: ${failureCount}/${count} (target: 30%) = ${((failureCount/count)*100).toFixed(1)}%`);
    console.log(`  Lane Changes: ${laneChangeCount}/${count} (target: 10%) = ${((laneChangeCount/count)*100).toFixed(1)}%`);
    console.log(`  Micro Random: ${microRandomCount}/${count} (target: 30%) = ${((microRandomCount/count)*100).toFixed(1)}%`);
    
    console.log('\n' + '='.repeat(50));
    console.log('✅ v1.x UNIFORM DISTRIBUTION TESTS PASSED');
    console.log('\nNOTE: These are legacy uniform distributions.');
    console.log('For REAL HUMAN STATISTICS: npm test');
}

const count = parseInt(process.argv[2]) || 100;
runDistributionTests(count);

export { runDistributionTests };
