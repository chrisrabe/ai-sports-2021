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
    for (const line of res) {
        const timerName = line.match(/Timer (.*):/)[1];
        const duration = line.match(/for (.*)ms/)[1];
        if (sums[timerName]) {
            sums[timerName] += parseFloat(duration);
        } else {
            sums[timerName] = parseFloat(duration);
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
    console.log(sums);
}).catch()
