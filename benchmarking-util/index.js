const lineReader = require('line-reader');
const filename = 'agent.logs';

const getTimerLines = new Promise(resolve => {
    const timerLines = [];
    lineReader.eachLine(filename, (line, last) => {
        if (line.includes('Timer')) {
            timerLines.push(line)
        }
        if (last) {
            resolve(timerLines);
        }
    })
});

getTimerLines.then(res => {
    const sums = {};
    const occurrence = {};
    const maxDuration = {};
    const minDuration = {};
    for (const line of res) {
        const timerName = line.match(/Timer (.*):/)[1];
        const duration = parseFloat(line.match(/for (.*)ms/)[1]);
        if (sums[timerName]) {
            sums[timerName] += duration
        } else {
            sums[timerName] = duration;
        }
        if (maxDuration[timerName]) {
            if (maxDuration[timerName] < duration) {
                maxDuration[timerName] = duration;
            }
        } else {
            maxDuration[timerName] = duration;
        }
        if (minDuration[timerName]) {
            if (minDuration[timerName] > duration) {
                minDuration[timerName] = duration
            }
        } else {
            minDuration[timerName] = duration;
        }
        if (occurrence[timerName]) {
            occurrence[timerName]++;
        } else {
            occurrence[timerName] = 1;
        }
    }
    for (const key of Object.keys(sums)) {
        sums[key] /= occurrence[key];
    }
    console.log('Maximum')
    console.log(maxDuration);
    console.log('Minimum')
    console.log(minDuration);
    console.log('Average executions')
    console.log(sums);
}).catch()
