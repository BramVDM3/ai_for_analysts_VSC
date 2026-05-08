# Interview Transcript: Front Desk Librarian

## Context

- Interview type: Semi-structured stakeholder interview
- Interview date: 2026-05-08
- Interviewer: Business analyst
- Participant: Front desk librarian
- Role: Handles book loans, returns, member questions, and desk support
- Current system discussed: Library web application currently used by staff

## Transcript

**Interviewer:** Thanks for taking the time. Could you start by describing how you use the application during a normal shift?

**Librarian:** Most of the time I use it for the basic things: checking the book list, checking members, creating a loan, and returning a book. The loan creation itself is actually quite straightforward. I pick a member, pick a book, choose the date, and the system creates the loan. That part is much better than the old spreadsheet days.

**Interviewer:** What works well about that flow?

**Librarian:** It is simple. There are not too many decisions on the screen. When someone is standing in front of you, that matters. You do not want five tabs and ten popups just to lend a book. I also like that the system already knows whether something is active or returned. Before, we sometimes had to infer that from empty cells.

**Interviewer:** And what is less smooth?

**Librarian:** The simple part is also the problem, I suppose. It creates one loan for one book. If a member comes with six books, you repeat the same thing six times. It is not hard, but it is annoying when there is a line. You also have to keep checking whether you selected the right member again. People get impatient.

**Interviewer:** How often does that happen?

**Librarian:** Every busy afternoon. Families, students before exams, older members after reading club. People rarely borrow exactly one book.

**Interviewer:** What happens when a member cannot borrow?

**Librarian:** That is one of the big frustrations. The system can block a loan, but it often feels like it just says no. Sometimes I can guess why. Maybe the book is reference-only. Maybe they already have too many loans. Maybe something is overdue. Maybe they are suspended. But I should not have to guess. The member asks me, "Why not?" and I am looking at the screen like it is a locked door.

**Interviewer:** What about books that never come back?

**Librarian:** That is another grey area. We can mark a loan as returned when the book comes back, but if the book is lost or just never returned, there is no clean process in the app. We keep notes outside the system or ask someone to remember it. Sometimes a book stays active forever because nobody wants to make the wrong change. That affects the catalogue too, because then other members ask why a book is unavailable for so long.

**Interviewer:** Is there a lost-book charge?

**Librarian:** In theory, yes, but in practice it is not handled nicely in the app. We need a way to say: this loan is not just late, it is lost or unresolved. And then we need to know what happens to the member, the book, and the amount owed. Right now that feels like desk folklore more than a process.

**Interviewer:** What do you do then?

**Librarian:** I check the member screen, then the loan list, then sometimes the book list. If I still cannot see it, I ask a colleague or tell the member we need to check later. That is embarrassing. It makes us look like we are hiding the rules.

**Interviewer:** Is there a member overview that helps?

**Librarian:** There is some member information, but I would not call it a complete desk overview. I can see loans, yes, but if someone has several active loans, returned loans, fines, and maybe a suspension date, I still have to piece together the story. I would like one place where I can answer: can this person borrow, what do they currently have, what do they owe, and what action can we take now?

**Interviewer:** You mentioned fines. How do you handle those today?

**Librarian:** Carefully. The system shows some pricing now, which helps, but when a member asks why they owe a specific amount, I still want the calculation broken down. Especially students. They say, "I thought it was free." And it is free at first, but after the free period they pay the daily price and the fine. If I cannot show that clearly, the conversation becomes a debate.

**Interviewer:** What would you want to see?

**Librarian:** Not a huge finance screen. Just enough detail: initial price, overdue days, daily price after due date, fine, total. Something I can point to. If it says 8.75 euro, show me why. Seven days times one euro plus seven days times twenty-five cents. That sort of thing.

**Interviewer:** Would you want that on the return screen?

**Librarian:** Yes, when returning a book is exactly when people ask. They do not ask two weeks earlier. They ask when I say there is a charge. The current return action is simple, which I like, but it would be good if the result clearly showed what changed financially.

**Interviewer:** How do members react to the pricing rules?

**Librarian:** Default members usually accept it. Seniors mostly ask us to explain it slowly, but they are not usually angry about the price. Students are different. They know the first period is free, and then suddenly it feels expensive. Some stop borrowing textbooks because they are afraid of forgetting. I understand them, honestly. A reminder would avoid half of those conversations.

**Interviewer:** Do you currently send reminders?

**Librarian:** Not from this app. We sometimes remind people manually if we know them, but that is not a process. It depends on who is at the desk and whether they have time. Students expect a notification. They live on notifications.

**Interviewer:** Do members use the application themselves?

**Librarian:** No, not really. It feels like a staff tool. Some members ask why they cannot check out books themselves, especially students. They are used to self-service everywhere. Personally, I see the benefit, but I am nervous about it.

**Interviewer:** Nervous in what way?

**Librarian:** If self-checkout is introduced badly, we will be the ones fixing mistakes. Wrong member, wrong book, book marked unavailable, payment confusion, blocked loans with no explanation. Also, some senior members will hate it. They come to us partly because they want help. The app should not make them feel pushed away.

**Interviewer:** So you want self-checkout or not?

**Librarian:** I want it for people who want it. I do not want it to replace the desk. Students should be able to do simple things themselves. Seniors should still be able to hand us a stack of books and talk to a human. The tricky part is that management hears "self-checkout" and thinks "less desk work." It might be more desk work at first.

**Interviewer:** How do you find information in the current UI?

**Librarian:** It is okay for basic lists, but some information is lower down than I expect. I scroll past the obvious part and then find the detail at the bottom. When the desk is busy, that feels backwards. If something is important during a loan or return, it should be near the action, not buried after a table.

**Interviewer:** Can you give an example?

**Librarian:** If I am returning a loan, I care about the return result, what the member owes, and whether the book becomes available again. If those are not visually close to the return action, I have to scan around. Same for member details. I do not want to hunt through a long loan table just to know the person has five active loans.

**Interviewer:** You said earlier you like that the app is simple. Would adding more information make it worse?

**Librarian:** That is the danger. Please do not turn it into an accounting system. I want more information, but only at the moment I need it. The main screen should stay calm. Maybe expand details when there is a problem, or show a small summary first. I know that sounds contradictory: keep it simple, but add more things. That is exactly how it feels at the desk.

**Interviewer:** How do you feel about the lending limits?

**Librarian:** I support having limits. Without limits, popular books disappear. But I need to know the limit and whether the member is near it. Right now the member just appears blocked. It would be better if I could see something like active loans count. I do not necessarily need a paragraph, but I need enough to explain the situation.

**Interviewer:** Should the member see that same explanation?

**Librarian:** Usually yes. Though for suspensions I am less sure. Some suspension reasons are sensitive. I do not want a big red banner with private details if someone else is looking over their shoulder. But "you cannot borrow until this date" would already help.

**Interviewer:** What about mobile?

**Librarian:** For members, yes. For staff at the desk, desktop is fine. A mobile app for members could show due dates, reminders, maybe whether a book is borrowable before they come in. But then the information has to match what we see. If the member's phone says one thing and my screen says another, the desk becomes a complaint counter.

**Interviewer:** What complaints do you hear most?

**Librarian:** Students complain about the free period ending. They say it is not visible enough. Some members complain that a book looked available but could not be borrowed. Others complain they were blocked without knowing why. And quite often people say they never got reminded. I cannot argue with that because they did not.

**Interviewer:** Are there features you definitely do not want?

**Librarian:** Anything that requires us to manage complex pricing tables every day. If the director wants different prices for different categories, memberships, events, workshops, whatever, that might be fine strategically, but please do not make the desk maintain it manually. We already have enough edge cases.

**Interviewer:** What would be your ideal improvement in the next version?

**Librarian:** A proper member desk overview. One screen. Current loans, active count, due dates, what is overdue, what they owe, whether they are blocked, and the reason in plain language. Then improve the return result so pricing is clear. After that, maybe batch loans, because one loan per book is tedious.

**Interviewer:** You put self-checkout after those?

**Librarian:** Yes. Self-checkout sounds exciting, but if the staff version still cannot explain blocks and prices, self-checkout will just make members confused faster.

**Interviewer:** Anything else students should understand from your perspective?

**Librarian:** The app is not bad. That is important. It is useful, and the simple loan flow is a good base. The frustration is mostly around exceptions. Normal loan, normal return, fine. But the library is full of exceptions: students, seniors, reference books, overdue books, five books at once, people who forgot, people who are embarrassed. A good system should stay simple when things are simple and become helpful when things are not.
