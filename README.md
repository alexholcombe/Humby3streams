Attentional Blink AND many-stream experiment implemented with [Psychopy](https://github.com/psychopy/psychopy), branched off from  [nStreams](https://github.com/alexholcombe/nStream).
============================
Licensing: MIT license, like CC-BY for code which means do whatever you want with it, with an attribution to the author.

This was created for Humby's honours thesis, so that she could run her first experiment with two or three simultaneous targets.


** NOTES **

- Alex work on handleAndScoreResponse for 2 cues but 3 streams, hence pay attention to whichStreamEachCue

- Only working now for 3 streams, lot of vestigial nonworking code for fewer/more streams

- whichStreamEachResp (and also whichRespEachCue) is set up by doRSVPstim

needs to be passed to lineu9p?

- angleBase determines which stream cued. Too complicated or is it working?