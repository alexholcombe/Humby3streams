Attentional Blink AND many-stream experiment implemented with [Psychopy](https://github.com/psychopy/psychopy), branched off from  [nStreams](https://github.com/alexholcombe/nStream).
============================
Licensing: MIT license, like CC-BY for code which means do whatever you want with it, with an attribution to the author.

This was created for Humby's honours thesis, so that she could run her first experiment with two or three simultaneous targets.


** NOTES **

- What's happening with counterbalancing of which stream respond to first in 3-target case? line 735

- Alex work on handleAndScoreResponse for 2 cues but 3 streams, hence pay attention to whichStreamEachCue
Needs to be out of 6 to counterbalance both 3 and 2-target conditions

-Also need to handle eyetracking


### Jen ###

* check it's really getting randomised
* check program's variation in serial position of targets, eg Kim's latest paper uses 5->12





### Random notes ###

- Only working now for 3 streams, lot of vestigial nonworking code for fewer/more streams

- whichStreamEachResp (and also whichRespEachCue) is set up by doRSVPstim
