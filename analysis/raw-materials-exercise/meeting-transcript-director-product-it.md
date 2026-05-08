# Meeting Transcript: Future App Direction Discussion

## Context

- Artifact type: Internal meeting transcript
- Date: 2026-05-11
- Participants:
  - Maria De Smet, Library Director
  - Anika Janssen, Product Manager
  - Pieter Vos, IT Lead
- Topic: What the future library direction means for the application
- Note: This transcript captures a realistic working discussion. Participants are professional, but frustration is visible.

## Transcript

**Maria, Director:** Thanks for joining. I sent the company-wide email because I want everyone to understand the broader direction. But we need a more practical conversation now. What does this mean for the app?

**Anika, Product Manager:** I am glad you asked it that way, because my first concern is that "community platform" can mean almost anything. Mobile app, self-checkout, reminders, events, dynamic pricing, membership tiers. These are all different products hiding inside one phrase.

**Maria:** I agree they are different, but they are connected. The library is more than lending. The app should reflect that.

**Pieter, IT Lead:** The app can reflect that eventually, but right now it is a small lending application. I am one person maintaining the backend. Every time we say "eventually", it still becomes my backlog.

**Maria:** I understand capacity is limited.

**Pieter:** I know you understand it, but the ideas keep arriving faster than the system can absorb them. Dynamic pricing alone is not small. Different book categories, member groups, exceptions, free periods, caps, reminders, payment disputes. That is not a setting. That is a policy engine.

**Anika:** And from the product side, we do not yet understand the current policy pain well enough. Students already do not understand the free period turning into daily charges and fines. Librarians cannot always explain why a member is blocked. If we add more pricing layers now, we are making a confusing thing more flexible, not better.

**Maria:** I do not want confusion. I want the app to support the library we are becoming.

**Anika:** Then we need sequencing. First make the existing lending rules understandable. Then member reminders. Then maybe member-facing self-service. Events and community can follow. But if we try to do everything in the next release, we will end up with a half-working app nobody trusts.

**Maria:** I am not asking for everything in one release.

**Pieter:** With respect, that is how it often lands. The strategy email mentions mobile, self-service, events, flexible memberships, and pricing. Staff will read that and ask when it is coming. Product will turn it into themes. Then someone asks IT for "just a simple version."

**Maria:** Fair. But we cannot only build what is easy for IT.

**Pieter:** I am not asking for easy. I am asking for maintainable. There is a difference. A bad configurable pricing system is worse than hard-coded rules. At least with hard-coded rules, I can test them. With a half-configurable system, someone changes a rule on Friday afternoon and Monday the desk is explaining wrong charges.

**Anika:** That is also an ownership question. Who owns pricing? The director? Product? Front desk? Finance? IT should not be the policy owner by default just because the rules live in code.

**Maria:** I agree IT should not own policy. But the rules need to be adaptable. We cannot ask members to wait six months for every policy change.

**Pieter:** Adaptable means process, not just software. Approval, test cases, rollback, audit history. If we do dynamic pricing later, fine. But then it needs proper governance. Otherwise it becomes "Pieter, can you quickly change the student fee?"

**Maria:** You are making it sound like the ambition itself is the problem.

**Pieter:** No. The ambition is not the problem. Pretending ambition has no operational cost is the problem.

**Anika:** I think that is the key conflict. Maria is right that the library needs a broader digital future. Pieter is right that we cannot build a platform by pretending it is still a simple app. And the librarians are already saying they want more details but also a simple desk workflow.

**Maria:** What would you do first, then?

**Anika:** A staff member overview. Not glamorous, but it addresses real pain. Active loans, loan count, due dates, blocks, current charges, and enough explanation to answer member questions. Then reminders before charges start, especially for students. Then a clearer return result showing price calculation.

**Maria:** That sounds very operational. Where is the future-facing part?

**Anika:** The future-facing part is trust. If members do not trust due dates, charges, or block reasons, they will not trust self-checkout or mobile. A mobile app that shows unclear rules is just a smaller unclear app.

**Pieter:** Also, the member overview gives us the service layer we need later. If we build it properly, mobile can reuse the same logic. If we jump straight to mobile, we duplicate confusion.

**Maria:** I can accept that. But I do not want events and community pushed away forever.

**Anika:** Not forever. But maybe separate track. Discovery of events is different from lending policy. It should not be blocked by overdue fine logic, and overdue fine logic should not be complicated by event registration.

**Pieter:** Please, yes. Keep those domains separate. Book lending, payments, events, memberships. They can connect, but if we mix them too early, we will regret it.

**Maria:** What about self-checkout?

**Anika:** Pilot with students, but only after block reasons and price previews are clear. Students want it. Seniors may not. Librarians are worried they will have to fix self-checkout mistakes. A pilot would let us test that instead of assuming.

**Pieter:** Self-checkout also needs permissions, fraud prevention, correction flows, and probably better book identification. If someone checks out the wrong book, who fixes it? If the app says blocked, do we show the reason? If it is a suspension, what privacy rules apply?

**Maria:** You are listing a lot of reasons not to do it.

**Pieter:** I am listing work. Some of it is necessary work.

**Anika:** And some of it is exactly what the analysts should extract from the interviews. The student will say "I want self-checkout." The senior will say "Please do not remove the desk." The librarian will say "Do not make me support a confusing self-checkout flow." Those are not contradictions to eliminate. They are constraints.

**Maria:** I like that framing.

**Pieter:** I can work with constraints. I struggle with slogans.

**Maria:** Point taken.

**Anika:** For the exercise material, I actually think this tension is useful. The director's ambition, the student's expectations, the senior's concerns, the librarian's desk reality, and IT's capacity limits should all be visible. Students should not be handed a neat list of requirements. They should have to interpret.

**Maria:** Agreed. But I still want them to see the strategic direction. Otherwise they will only optimize the current desk process.

**Pieter:** And I want them to see the cost of every "just add" request.

**Anika:** Then we have our structure. Broad vision in the email. Messy trade-offs in the meeting transcript. Interviews and complaints for grounded evidence. Data and incomplete models for system evidence.

**Maria:** Good. For the next phase, let us say: immediate focus on lending transparency, reminders, member overview, and return pricing clarity. Strategic exploration of mobile, self-checkout, events, and flexible membership. Dynamic pricing stays an option, but not without governance.

**Pieter:** And tests.

**Maria:** And tests.

**Anika:** I will write that down exactly.
