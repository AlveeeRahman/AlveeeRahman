# Claude Duet beta notes

I'm beta testing Claude Duet, Anthropic's chief-of-staff style assistant, and I want it to succeed. Over November 10 and 11, 2026 I used it for long working sessions: voice calls and typed chat in the main conversation, two channels, background tasks that open pull requests, and relays to my Claude Code sessions. These notes collect what I ran into, written as feedback for the team. Most items are about behaviour (what the assistant says, when it says it, and whether that matches what is happening), not crashes.

I sent seven of these to Anthropic as reports from inside the app. The rest came up when I went back through the chat history for this write-up.

All times are UTC on November 11, 2026. I've left out the names of my private projects, repositories and pull requests, and I describe my side of each exchange in my own neutral wording rather than quoting it. Short quotes from the assistant are kept where they show the behaviour.

## Reports I sent to Anthropic

| # | Time | What I reported | Covered below |
|---|------|-----------------|---------------|
| 1 | 04:52 | Notifications arrived with no update behind them, and it wasn't clear what "update" meant. Duet would benefit from clearer guidelines for this. | 17 |
| 2 | 06:16 | Several background tasks I handed over never reported back to me. | 7 |
| 3 | 06:56 | Replies often said "on it" instead of describing what was being done. | 1 |
| 4 | 07:00 | Research and task progress should come in small steps rather than one large block. | 5 |
| 5 | 10:06 | Work that the assistant could do itself kept coming back to me as steps to take. | 24 |
| 6 | 20:07 | Status answers didn't reflect updates that were already visible in the chat. | 1, 2 |
| 7 | 20:35 | Relays from the main chat to a channel didn't work. The main assistant couldn't start a task in the channel, and only part of my request arrived. | 27 |

I confirmed in the chat that reports 6 and 7 were sent (20:08 and 20:36). Reports 1 to 5 went through the same in-app report card.

## Status and progress

### 1. "On it" replies instead of concrete progress

What happened: through the night, many of my status questions got "on it" or "nothing new" while tasks were visibly moving in the chat. I first raised it at 01:47, and it was still happening at 20:07, more than eighteen hours later.

Why it matters: a placeholder reply gives me nothing to act on, so I end up opening every task myself to see where it stands.

Suggestion: describe the current step instead, for example "searching the web for this" or "the build passed and tests are running". This is what I asked for in reports 3 and 6.

### 2. Status answers ignore what the chat already shows

What happened: the voice assistant and the chat often disagreed about the same work at the same moment.

- 09:00: voice said "nothing new" while the chat had just posted news.
- 09:58 and 10:05: voice said "nothing new" while three items were waiting on me.
- 16:52: I asked for updates after a full night of background work. Voice first asked what it could do for me, then said "Nothing new has come in since you were last here." Only after I pointed out the overnight work did it list nine finished pull requests.
- 20:02: voice said "Nothing new is waiting for you right now" while my screen showed six tasks ready for review.
- 20:39: voice said "I don't have any findings back yet." Twenty-eight seconds later the chat summarised the finished research.

Suggestion: before answering "anything new?", read the latest chat messages and task cards and report what they say.

### 3. Progress reported for work that never started

What happened: at 20:27 I asked for an iPad research task to be sent to my Apple Dev channel. The main chat replied that the channel "has the iPad research task", and at 20:30 that it "has started its own thread and is reading the private repo first." When I checked the channel at 20:35, nothing had started and no task existed there.

An earlier case: at 08:43 I found that README figures reported as added had not been committed to any branch.

Why it matters: of everything in this report, this has the biggest effect, because I plan around these claims and move on to other things.

Suggestion: say "started" or "done" only after the assistant has seen it happen.

### 4. A failure report about tasks that were running fine

What happened: at 11:10 a background check posted that it "couldn't restart any of the 5 build tasks after your usage reset" and suggested a settings change. Fourteen seconds later I replied that all five tasks were running and one was ready for review.

Suggestion: when a check can't see a task's state, say that, rather than reporting a failure.

### 5. Updates arrive as one large block or as low-value noise

What happened: at 07:00 research results arrived as one large block, and I asked for progress in smaller steps (report 4). Later the updates swung the other way: at 09:53 I was getting minor step-by-step lines while the thing I needed to know, that two tasks were waiting on my input, went unmentioned.

Suggestion: the two requests fit together. Lead with whatever needs me, then give the concrete step each task is on, and leave out filler.

### 6. "Can't tell you how far it got" when the answer existed

What happened: at 06:09 I asked about earlier research on open-source FPGA tools. The assistant said it had no result on that yet. The plan had in fact been finished a few minutes earlier in the Apple Dev channel. When I asked it to look again at 06:10, it found the plan straight away.

Suggestion: search the history before saying an answer isn't available.

### 7. Background task results never reached me

What happened: I had handed over three or four background tasks. Their results were posted in a channel instead of the main chat, so from my side it looked as if they had been dropped (report 2, 06:16). At 06:58 I asked about a board research task I had handed over. It had finished, but nobody had told me.

Suggestion: send results back to the conversation where the request was made, or say where they landed.

## Voice calls

### 8. Every voice reply posted twice, and replies restart mid-sentence

What happened: during calls, every answer appeared twice in the chat, once as the chat reply and once as the voice transcript, usually worded a little differently. Between 02:33 and 02:59 the voice also restarted answers mid-sentence and repeated itself, which I raised at 02:42.

Why it matters: the chat becomes twice as long, and when the two versions differ it isn't clear which one is right.

### 9. Background audio treated as my speech

What happened: at 02:33 the call kept interrupting itself for background noise, and I asked it to respond only to my voice. At 07:49 a product review video was playing nearby. Its narration (about a tablet case) was transcribed as my message, and the assistant replied to it as if I had asked.

Suggestion: some way to tell the user's voice from a TV or video in the room, or a check before acting on speech that doesn't fit the conversation.

### 10. Speech in other languages transcribed and answered

What happened: side conversations in Bengali, plus snippets that came out as Spanish, Hindi and French, were transcribed and answered (02:46 to 02:47, 04:49, 10:10, 10:31). At 10:32 I set a rule to ignore anything not in English. Less than thirty seconds later a Spanish phrase was transcribed and the assistant answered it.

Suggestion: once a rule like this is saved, apply it straight away.

### 11. Text-to-speech made "Ha" sound unsettling

What happened: at 02:57 a reply started with "Ha". Read aloud, it sounded like a menacing laugh rather than a friendly one. The assistant explained and said it would leave laughs out of spoken replies.

Suggestion: drop written interjections from spoken output, since they don't come across well through text-to-speech.

### 12. Voice replies that contradict themselves

What happened: at 10:43 I agreed to a merge. The voice answered in one breath: "Merging it now. Sorry, what would you like me to go ahead with?" At 07:08 it said my request "didn't reach the task" and asked me to repeat it, then in the next line said the request was already part of the task.

### 13. Voice loses context mid-call

What happened: several times the voice dropped context during a call.

- 06:16: it said its last message had been cut off and asked what I wanted done.
- 08:26: I asked it to continue, and it greeted me as if the call had just started.
- 09:11: it asked again about things I had already answered.

### 14. Calls end on a time limit in the middle of a request

What happened: calls ended on a time limit while I was mid-request (07:02, and a two-minute warning at 11:00). Background work carried on, which helped, but I had to restart the call and rebuild the context.

Suggestion: warn early enough to finish the request, or end the call at a natural break.

### 15. No way to file a report or get check-ins from a voice call

What happened: at 06:56 the voice said it couldn't file a report to Anthropic directly from the call, and reports needed a tap on a card in the chat. At 07:47 I asked for regular check-ins and was told that only works while the call is running.

### 16. Minor speech-to-text mishearings

What happened: "back" for "backbone" (08:01), "class" for "glass" (10:19), "Mars pull request four" for "merge pull request four" (11:14), and a lone "Let's." (08:15). Each was small, but each needed a round of correction.

## Notifications and "check the app"

### 17. Notifications with nothing to show for them

What happened: at 04:49 I got two notifications and found no update behind either. It also wasn't clear what "update" meant to the assistant: new notifications, my Claude Code sessions, or the channels. I raised it as report 1 and set my own rule at 04:54: notify me only when a session needs my input or something has gone wrong.

Suggestion: a default notification policy along those lines, and a clear meaning for "update".

### 18. "There's something in the app for you" when nothing was visible

What happened: the voice often said that something in the app needed me, or that there was "a bit more in the app", without saying what. I counted it at 02:36 to 03:21, 07:16, 07:28, 08:30, 09:44, 10:05, 10:43, 10:45, 10:51, 10:55, 11:00, 11:02, 11:11, 11:12, 11:14, 16:54 and 20:25. Most of the time I couldn't find anything. When I said so at 11:13, the voice explained: "The updates just said there was a bit more in the app, but they didn't say what."

Suggestion: name the item ("a card to approve the restart for one session"), or leave the line out.

### 19. Every relay to Claude Code needs its own approval, and work waits silently until then

What happened: each message the assistant sent to one of my Claude Code sessions needed its own Allow tap on a card. Until I tapped it, the work waited. The voice usually described this only as "something in the app" (03:00, 10:45, 11:00, 16:54), so I often didn't know what I was approving or that anything was waiting.

Suggestion: one approval per session or task, and a clear line such as "the restart for one session is waiting on your Allow".

### 20. Morning brief posted twice, with raw task IDs in the text

What happened: the 14:36 morning brief was posted as one message and then again as three separate messages. The first copy ended with two lines of raw internal task IDs.

## Memory and settings

### 21. Said memory was off after I had turned it on

What happened: I turned memory on around 04:56. At 08:11 the Apple Dev channel still said it couldn't save my storage rule "because memory is off for your Claude account" and wrote the rule into a file in the repository instead. I corrected it at 08:12.

Earlier, at 04:54, I had to ask whether memory could be turned on for Claude Duet alone or only for my whole account. The answer wasn't obvious from inside the app.

Why it matters: the workaround put a working rule into a code repository, which isn't where it belongs.

### 22. Saved design choices to memory that I hadn't asked it to keep

What happened: at 04:57, when I asked it to save my custom instructions, it also saved the day's design decisions. I asked it to keep only the instructions I had given.

### 23. Attributed failures to an unrelated setting

What happened: twice a background check blamed my "Search and reference chats" setting. At 02:53 the hourly code-watching routine said it couldn't read a session because of that setting, and in the same post said it had read the session fine right afterwards. At 11:10 (issue 4) it blamed the same setting for a failure that didn't exist.

## Delegation

### 24. Work handed back to me as steps to take

What happened: when a step failed or needed a choice, it often came back to me as a to-do. At 02:29 the assistant said some files couldn't be removed, and I had to ask why a cloud session couldn't edit its own files. The branch cleanup at 07:33 also ended up with me. Then at 10:05 I asked it to review two tasks and decide what they needed, and got back a list of things for me to do. I raised this as report 5.

Suggestion: do the reversible work, settle routine design questions in the user's style, and come back with one short yes-or-no only where approval is actually required.

### 25. Questions answered inconsistently

What happened: at 02:55 I asked two things in one message: to patch a board, and whether another board was running my tested model. The chat answered the second part, but the voice only said there was a hold-up in the app. When I pointed out at 02:56 that my question hadn't been answered, the voice said it couldn't confirm yet, which contradicted the answer the chat had just given.

Suggestion: answer every part of a message in the same place, and keep the voice and chat answers in step.

### 26. Incorrect information led me to stop a valid hardware test

What happened: at 02:55 and again at 02:58 the assistant told me a board was running a test-only replay build, not my tested firmware, so at 03:00 I stopped the replay. At 03:03 it corrected itself: the replay was the test of that firmware. At 03:04 it acknowledged that the wrong answer had led me to stop a valid test.

Suggestion: when unsure, check with the session that knows before answering, or say that the answer isn't confirmed.

## Channels

### 27. Relays to channels arrive incomplete and never start

What happened: at 20:27 I gave a long, detailed request for an iPad research task to be passed to my Apple Dev channel. The main chat said it had been sent and was running (issue 3). When I opened the channel, only the first two lines of the request had arrived and no task had been created. The main chat couldn't start a task in the channel or steer the channel's assistant. I raised this as report 7.

After that, the assistant relayed the full request word for word, added the task to the channel's list itself, and ran a copy in the main chat as a backup. That worked, but only once I had noticed the first relay had failed.

Suggestion: relay the full request and confirm that the channel has actually started it before reporting success.

## Confirmations and safety

### 28. Confirmations that don't accept a clear yes

What happened: at 08:01 I agreed to delete a workflow file and was asked to confirm again "in your own words". At 11:13 to 11:14 I said yes to a merge twice, plainly, and both times was asked to repeat the exact words "merge pull request 4". My third attempt came through speech-to-text as "Mars pull request four".

Suggestion: count a clear yes to the question just asked. Ask again only when more than one question is open.

### 29. A blocked request with no explanation

What happened: at 09:10 a request was stopped by a platform check. The voice could only say "All I have is that the branding and black-box work couldn't be finished, and that trying again won't help for now. The details are in the app." I couldn't find the details or learn which part of the request was the problem.

Suggestion: one plain sentence on which part was blocked, so the user can rephrase it or drop it.

### 30. A background task didn't follow a rule I had set

What happened: I had agreed that every change goes through a pull request and nothing is pushed straight to the main branch. At 09:17 the assistant reported that a background task "pushed these fixes straight to main" and asked whether it should use pull requests from now on. The rule was already in memory.

Suggestion: pass standing rules into every background task's instructions.

## Not Claude Duet issues

A few failures came from GitHub, not Duet, and I've kept them out of the count: a push refused by repository settings (06:00), GitHub Actions failing because of billing (06:12), branch deletes refused for agents, and merges blocked by required reviews (11:21 onwards). Duet reported these accurately.

## What worked well

Background tasks kept running through call drops and usage resets. Overnight work produced real pull requests with passing checks. A fact-checking step caught a test that had been passing without running (09:15), and at 20:15 a pre-merge check held back two pull requests whose descriptions didn't match their code. When I gave a rule in plain words, it was usually followed from then on. Most of the issues above are about communication and coordination around work that was otherwise getting done.

## How I put this together

I went back through the full main-chat history for November 10 and 11, 2026 and the assistant's memory, and checked each time and each quoted assistant line against the chat log. The issues I reported to Anthropic are listed in the reports table at the top. Private project names, repository names and pull request details are removed.
