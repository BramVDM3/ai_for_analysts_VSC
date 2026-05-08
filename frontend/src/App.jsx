import { useEffect, useMemo, useState } from "react";

const PAGE_LABELS = {
  lending: "Lending",
  books: "Books",
  members: "Members",
  loans: "Loans",
};

const blankLoanForm = {
  memberId: "",
  bookId: "",
  loanDate: "",
};

const blankBookForm = {
  title: "",
  category: "",
  available: true,
  referenceOnly: false,
};

const blankMemberForm = {
  firstName: "",
  lastName: "",
  email: "",
  memberType: "default",
  suspendedUntil: "",
};

function App() {
  const [activePage, setActivePage] = useState(getInitialPage);
  const [health, setHealth] = useState(null);
  const [healthLoading, setHealthLoading] = useState(false);
  const [healthError, setHealthError] = useState(null);
  const [books, setBooks] = useState([]);
  const [booksLoading, setBooksLoading] = useState(true);
  const [booksError, setBooksError] = useState(null);
  const [members, setMembers] = useState([]);
  const [membersLoading, setMembersLoading] = useState(true);
  const [membersError, setMembersError] = useState(null);
  const [memberOverview, setMemberOverview] = useState(null);
  const [memberOverviewLoading, setMemberOverviewLoading] = useState(false);
  const [memberOverviewError, setMemberOverviewError] = useState(null);
  const [loans, setLoans] = useState([]);
  const [loansLoading, setLoansLoading] = useState(true);
  const [loansError, setLoansError] = useState(null);
  const [loanForm, setLoanForm] = useState(blankLoanForm);
  const [loanCreateLoading, setLoanCreateLoading] = useState(false);
  const [loanCreateError, setLoanCreateError] = useState(null);
  const [createdLoan, setCreatedLoan] = useState(null);
  const [loanReturnLoadingId, setLoanReturnLoadingId] = useState(null);
  const [loanReturnError, setLoanReturnError] = useState(null);
  const [returnedLoan, setReturnedLoan] = useState(null);
  const [bookSearch, setBookSearch] = useState("");
  const [bookAvailabilityFilter, setBookAvailabilityFilter] = useState("all");
  const [bookUseFilter, setBookUseFilter] = useState("all");
  const [bookFormMode, setBookFormMode] = useState(null);
  const [bookForm, setBookForm] = useState(blankBookForm);
  const [bookFormError, setBookFormError] = useState(null);
  const [memberSearch, setMemberSearch] = useState("");
  const [memberTypeFilter, setMemberTypeFilter] = useState("all");
  const [memberSuspensionFilter, setMemberSuspensionFilter] = useState("all");
  const [memberFormMode, setMemberFormMode] = useState(null);
  const [memberForm, setMemberForm] = useState(blankMemberForm);
  const [memberFormError, setMemberFormError] = useState(null);
  const [loanSearch, setLoanSearch] = useState("");
  const [loanStatusFilter, setLoanStatusFilter] = useState("all");
  const [loanDueFilter, setLoanDueFilter] = useState("all");

  useEffect(() => {
    loadBooks();
    loadMembers();
    loadLoans();
  }, []);

  useEffect(() => {
    const handleHashChange = () => setActivePage(getInitialPage());
    window.addEventListener("hashchange", handleHashChange);
    return () => window.removeEventListener("hashchange", handleHashChange);
  }, []);

  const visibleBooks = useMemo(
    () =>
      books.filter((book) => {
        const search = bookSearch.trim().toLowerCase();
        const matchesSearch =
          !search ||
          book.bookId.toLowerCase().includes(search) ||
          book.title.toLowerCase().includes(search);
        const matchesAvailability =
          bookAvailabilityFilter === "all" ||
          (bookAvailabilityFilter === "available" && book.available) ||
          (bookAvailabilityFilter === "unavailable" && !book.available);
        const matchesUse =
          bookUseFilter === "all" ||
          (bookUseFilter === "regular" && !book.referenceOnly) ||
          (bookUseFilter === "reference" && book.referenceOnly);

        return matchesSearch && matchesAvailability && matchesUse;
      }),
    [books, bookAvailabilityFilter, bookSearch, bookUseFilter]
  );

  const visibleMembers = useMemo(
    () =>
      members.filter((member) => {
        const search = memberSearch.trim().toLowerCase();
        const fullName = `${member.firstName} ${member.lastName}`.toLowerCase();
        const matchesSearch =
          !search ||
          member.memberId.toLowerCase().includes(search) ||
          member.firstName.toLowerCase().includes(search) ||
          member.lastName.toLowerCase().includes(search) ||
          fullName.includes(search) ||
          member.email.toLowerCase().includes(search);
        const matchesType =
          memberTypeFilter === "all" || member.memberType === memberTypeFilter;
        const matchesSuspension =
          memberSuspensionFilter === "all" ||
          (memberSuspensionFilter === "suspended" && member.suspendedUntil) ||
          (memberSuspensionFilter === "not-suspended" && !member.suspendedUntil);

        return matchesSearch && matchesType && matchesSuspension;
      }),
    [memberSearch, memberSuspensionFilter, memberTypeFilter, members]
  );

  const visibleLoans = useMemo(
    () =>
      loans.filter((loan) => {
        const search = loanSearch.trim().toLowerCase();
        const matchesSearch =
          !search ||
          loan.loanId.toLowerCase().includes(search) ||
          loan.bookId.toLowerCase().includes(search) ||
          loan.memberId.toLowerCase().includes(search);
        const matchesStatus =
          loanStatusFilter === "all" || loan.status === loanStatusFilter;
        const matchesDue = matchesDueFilter(loan, loanDueFilter);

        return matchesSearch && matchesStatus && matchesDue;
      }),
    [loanDueFilter, loanSearch, loanStatusFilter, loans]
  );

  const readJsonResponse = async (response, fallbackMessage) => {
    try {
      return await response.json();
    } catch {
      throw new Error(fallbackMessage);
    }
  };

  const checkBackend = async () => {
    setHealthLoading(true);
    setHealthError(null);
    try {
      const response = await fetch("/api/health");
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const data = await response.json();
      setHealth(data.status);
    } catch (err) {
      setHealthError(err.message);
      setHealth(null);
    } finally {
      setHealthLoading(false);
    }
  };

  const loadBooks = async () => {
    setBooksLoading(true);
    setBooksError(null);
    try {
      const response = await fetch("/api/books");
      const data = await readJsonResponse(
        response,
        "Book catalogue data could not be loaded."
      );

      if (!response.ok) {
        throw new Error(data.message || `HTTP ${response.status}`);
      }

      if (!Array.isArray(data)) {
        throw new Error("Book catalogue data could not be loaded.");
      }

      setBooks(data);
    } catch (err) {
      setBooks([]);
      setBooksError(err.message);
    } finally {
      setBooksLoading(false);
    }
  };

  const loadMembers = async () => {
    setMembersLoading(true);
    setMembersError(null);
    try {
      const response = await fetch("/api/members");
      const data = await readJsonResponse(
        response,
        "Member list data could not be loaded."
      );

      if (!response.ok) {
        throw new Error(data.message || `HTTP ${response.status}`);
      }

      if (!Array.isArray(data)) {
        throw new Error("Member list data could not be loaded.");
      }

      setMembers(data);
    } catch (err) {
      setMembers([]);
      setMembersError(err.message);
    } finally {
      setMembersLoading(false);
    }
  };

  const loadLoans = async () => {
    setLoansLoading(true);
    setLoansError(null);
    try {
      const response = await fetch("/api/loans");
      const data = await readJsonResponse(
        response,
        "Loan list data could not be loaded."
      );

      if (!response.ok) {
        throw new Error(data.message || `HTTP ${response.status}`);
      }

      if (!Array.isArray(data)) {
        throw new Error("Loan list data could not be loaded.");
      }

      setLoans(data);
    } catch (err) {
      setLoans([]);
      setLoansError(err.message);
    } finally {
      setLoansLoading(false);
    }
  };

  const openMemberOverview = async (memberId) => {
    setMemberOverviewLoading(true);
    setMemberOverviewError(null);
    try {
      const response = await fetch(`/api/members/${memberId}/overview`);
      const data = await readJsonResponse(
        response,
        "Member overview could not be loaded."
      );

      if (!response.ok) {
        throw new Error(data.message || `HTTP ${response.status}`);
      }

      if (!data || !data.member || !Array.isArray(data.loans)) {
        throw new Error("Member overview could not be loaded.");
      }

      setMemberOverview(data);
    } catch (err) {
      setMemberOverview(null);
      setMemberOverviewError(err.message);
    } finally {
      setMemberOverviewLoading(false);
    }
  };

  const goToPage = (page) => {
    window.location.hash = page;
    setActivePage(page);
  };

  const updateLoanForm = (field, value) => {
    setLoanForm((current) => ({ ...current, [field]: value }));
    setLoanCreateError(null);
  };

  const submitLoanForm = async (event) => {
    event.preventDefault();
    setCreatedLoan(null);
    setLoanCreateError(null);

    if (!loanForm.memberId) {
      setLoanCreateError("Select a member before creating a loan.");
      return;
    }

    if (!loanForm.bookId) {
      setLoanCreateError("Select a book before creating a loan.");
      return;
    }

    if (!loanForm.loanDate) {
      setLoanCreateError("Enter the loan date.");
      return;
    }

    setLoanCreateLoading(true);
    try {
      const response = await fetch("/api/loans", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(loanForm),
      });
      const data = await readJsonResponse(response, "Loan could not be created.");

      if (!response.ok) {
        if (response.status === 405) {
          throw new Error(
            "Loan creation is not available at this route. Check that the frontend is using the /api proxy and that the backend exposes POST /loans."
          );
        }
        throw new Error(data.message || `HTTP ${response.status}`);
      }

      if (!data || !data.loanId || data.status !== "active") {
        throw new Error("Loan could not be created.");
      }

      setCreatedLoan(data);
      await loadLoans();
      await loadBooks();

      if (memberOverview?.member?.memberId === data.memberId) {
        await openMemberOverview(data.memberId);
      }
    } catch (err) {
      setLoanCreateError(err.message);
    } finally {
      setLoanCreateLoading(false);
    }
  };

  const returnLoan = async (loan) => {
    setLoanReturnError(null);
    setReturnedLoan(null);
    setLoanReturnLoadingId(loan.loanId);

    try {
      const response = await fetch(`/api/loans/${loan.loanId}/return`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          returnDate: new Date().toISOString().slice(0, 10),
        }),
      });
      const data = await readJsonResponse(
        response,
        "Loan could not be marked as returned."
      );

      if (!response.ok) {
        throw new Error(data.message || `HTTP ${response.status}`);
      }

      if (!data || data.status !== "returned") {
        throw new Error("Loan could not be marked as returned.");
      }

      setReturnedLoan(data);
      await loadLoans();
      await loadBooks();

      if (memberOverview?.member?.memberId === data.memberId) {
        await openMemberOverview(data.memberId);
      }
    } catch (err) {
      setLoanReturnError(err.message);
    } finally {
      setLoanReturnLoadingId(null);
    }
  };

  const startAddBook = () => {
    setBookFormMode({ type: "add" });
    setBookForm(blankBookForm);
    setBookFormError(null);
  };

  const startEditBook = (book) => {
    setBookFormMode({ type: "edit", id: book.bookId });
    setBookForm({
      title: book.title,
      category: book.category,
      available: book.available,
      referenceOnly: book.referenceOnly,
    });
    setBookFormError(null);
  };

  const saveBook = (event) => {
    event.preventDefault();
    if (!bookForm.title.trim()) {
      setBookFormError("Book title is required.");
      return;
    }
    if (!bookForm.category.trim()) {
      setBookFormError("Book category is required.");
      return;
    }

    if (bookFormMode?.type === "edit") {
      setBooks((current) =>
        current.map((book) =>
          book.bookId === bookFormMode.id
            ? { ...book, ...bookForm, title: bookForm.title.trim(), category: bookForm.category.trim() }
            : book
        )
      );
    } else {
      setBooks((current) => [
        ...current,
        {
          bookId: nextId(current, "bookId", "B"),
          title: bookForm.title.trim(),
          category: bookForm.category.trim(),
          available: bookForm.available,
          referenceOnly: bookForm.referenceOnly,
        },
      ]);
    }

    setBookFormMode(null);
    setBookForm(blankBookForm);
    setBookFormError(null);
  };

  const startAddMember = () => {
    setMemberFormMode({ type: "add" });
    setMemberForm(blankMemberForm);
    setMemberFormError(null);
  };

  const startEditMember = (member) => {
    setMemberFormMode({ type: "edit", id: member.memberId });
    setMemberForm({
      firstName: member.firstName,
      lastName: member.lastName,
      email: member.email,
      memberType: member.memberType,
      suspendedUntil: member.suspendedUntil || "",
    });
    setMemberFormError(null);
  };

  const saveMember = (event) => {
    event.preventDefault();
    if (!memberForm.firstName.trim()) {
      setMemberFormError("First name is required.");
      return;
    }
    if (!memberForm.lastName.trim()) {
      setMemberFormError("Last name is required.");
      return;
    }
    if (!memberForm.email.trim() || !memberForm.email.includes("@")) {
      setMemberFormError("A valid email is required.");
      return;
    }
    if (!memberForm.memberType) {
      setMemberFormError("Member type is required.");
      return;
    }

    const normalizedMember = {
      ...memberForm,
      firstName: memberForm.firstName.trim(),
      lastName: memberForm.lastName.trim(),
      email: memberForm.email.trim(),
      suspendedUntil: memberForm.suspendedUntil || null,
    };

    if (memberFormMode?.type === "edit") {
      setMembers((current) =>
        current.map((member) =>
          member.memberId === memberFormMode.id
            ? { ...member, ...normalizedMember }
            : member
        )
      );
    } else {
      setMembers((current) => [
        ...current,
        {
          memberId: nextId(current, "memberId", "M"),
          createdAt: new Date().toISOString().slice(0, 10),
          ...normalizedMember,
        },
      ]);
    }

    setMemberFormMode(null);
    setMemberForm(blankMemberForm);
    setMemberFormError(null);
  };

  const clearBookFilters = () => {
    setBookSearch("");
    setBookAvailabilityFilter("all");
    setBookUseFilter("all");
  };

  const clearMemberFilters = () => {
    setMemberSearch("");
    setMemberTypeFilter("all");
    setMemberSuspensionFilter("all");
  };

  const clearLoanFilters = () => {
    setLoanSearch("");
    setLoanStatusFilter("all");
    setLoanDueFilter("all");
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <h1>Library</h1>
          <span>Catalogue</span>
        </div>

        <nav className="nav" aria-label="Main areas">
          {Object.entries(PAGE_LABELS).map(([page, label]) => (
            <button
              className={activePage === page ? "nav-link active" : "nav-link"}
              key={page}
              onClick={() => goToPage(page)}
              type="button"
            >
              {label}
            </button>
          ))}
        </nav>

        <section className="health-panel" aria-label="Backend tools">
          <button onClick={checkBackend} disabled={healthLoading} type="button">
            {healthLoading ? "Checking..." : "Check backend"}
          </button>
          {health && <div className="status success">Backend: {health}</div>}
          {healthError && <div className="status error">Error: {healthError}</div>}
        </section>
      </aside>

      <main className="content">
        <header className="top-banner" aria-label="Library workspace banner">
          <div className="library-logo" aria-hidden="true">
            <span />
            <span />
            <span />
          </div>
          <div>
            <p className="banner-kicker">Librarian workspace</p>
            <h2>Northbridge Public Library</h2>
          </div>
        </header>

        {activePage === "lending" && (
          <LendingPage
            books={books}
            booksError={booksError}
            booksLoading={booksLoading}
            createdLoan={createdLoan}
            loanCreateError={loanCreateError}
            loanCreateLoading={loanCreateLoading}
            loanForm={loanForm}
            members={members}
            membersError={membersError}
            membersLoading={membersLoading}
            onSubmit={submitLoanForm}
            onUpdate={updateLoanForm}
          />
        )}

        {activePage === "books" && (
          <BooksPage
            availabilityFilter={bookAvailabilityFilter}
            booksError={booksError}
            booksLoading={booksLoading}
            clearFilters={clearBookFilters}
            form={bookForm}
            formError={bookFormError}
            formMode={bookFormMode}
            onCancelForm={() => setBookFormMode(null)}
            onEdit={startEditBook}
            onFormChange={setBookForm}
            onSave={saveBook}
            onStartAdd={startAddBook}
            onUpdateAvailability={setBookAvailabilityFilter}
            onUpdateSearch={setBookSearch}
            onUpdateUse={setBookUseFilter}
            search={bookSearch}
            useFilter={bookUseFilter}
            visibleBooks={visibleBooks}
          />
        )}

        {activePage === "members" && (
          <MembersPage
            clearFilters={clearMemberFilters}
            form={memberForm}
            formError={memberFormError}
            formMode={memberFormMode}
            memberOverview={memberOverview}
            memberOverviewError={memberOverviewError}
            memberOverviewLoading={memberOverviewLoading}
            membersError={membersError}
            membersLoading={membersLoading}
            onCancelForm={() => setMemberFormMode(null)}
            onEdit={startEditMember}
            onFormChange={setMemberForm}
            onOpenOverview={openMemberOverview}
            onSave={saveMember}
            onStartAdd={startAddMember}
            onUpdateSearch={setMemberSearch}
            onUpdateSuspension={setMemberSuspensionFilter}
            onUpdateType={setMemberTypeFilter}
            search={memberSearch}
            suspensionFilter={memberSuspensionFilter}
            typeFilter={memberTypeFilter}
            visibleMembers={visibleMembers}
          />
        )}

        {activePage === "loans" && (
          <LoansPage
            clearFilters={clearLoanFilters}
            dueFilter={loanDueFilter}
            loansError={loansError}
            loansLoading={loansLoading}
            loanReturnError={loanReturnError}
            loanReturnLoadingId={loanReturnLoadingId}
            onReturnLoan={returnLoan}
            onUpdateDue={setLoanDueFilter}
            onUpdateSearch={setLoanSearch}
            onUpdateStatus={setLoanStatusFilter}
            returnedLoan={returnedLoan}
            search={loanSearch}
            statusFilter={loanStatusFilter}
            visibleLoans={visibleLoans}
          />
        )}
      </main>
    </div>
  );
}

function LendingPage({
  books,
  booksError,
  booksLoading,
  createdLoan,
  loanCreateError,
  loanCreateLoading,
  loanForm,
  members,
  membersError,
  membersLoading,
  onSubmit,
  onUpdate,
}) {
  return (
    <section className="page lending-page" aria-labelledby="lending-heading">
      <PageHeader
        id="lending-heading"
        title="Lending"
        subtitle="Create a loan for a member and a book."
      />

      {(booksError || membersError) && (
        <div className="status error">Loan choices could not be loaded.</div>
      )}

      <form className="loan-form primary-form" onSubmit={onSubmit}>
        <label>
          <span>Member</span>
          <select
            value={loanForm.memberId}
            onChange={(event) => onUpdate("memberId", event.target.value)}
            disabled={membersLoading || Boolean(membersError) || loanCreateLoading}
          >
            <option value="">Select member</option>
            {members.map((member) => (
              <option key={member.memberId} value={member.memberId}>
                {member.memberId} - {member.firstName} {member.lastName}
              </option>
            ))}
          </select>
        </label>

        <label>
          <span>Book</span>
          <select
            value={loanForm.bookId}
            onChange={(event) => onUpdate("bookId", event.target.value)}
            disabled={booksLoading || Boolean(booksError) || loanCreateLoading}
          >
            <option value="">Select book</option>
            {books.map((book) => (
              <option
                disabled={!canLoanBook(book)}
                key={book.bookId}
                value={book.bookId}
              >
                {book.bookId} - {book.title} ({bookStatusLabel(book)})
              </option>
            ))}
          </select>
        </label>

        <label>
          <span>Loan date</span>
          <input
            type="date"
            value={loanForm.loanDate}
            onChange={(event) => onUpdate("loanDate", event.target.value)}
            disabled={loanCreateLoading}
          />
        </label>

        <button
          type="submit"
          disabled={
            loanCreateLoading ||
            booksLoading ||
            membersLoading ||
            Boolean(booksError) ||
            Boolean(membersError)
          }
        >
          {loanCreateLoading ? "Creating loan..." : "Create loan"}
        </button>
      </form>

      {loanCreateError && (
        <div className="status error">Loan creation error: {loanCreateError}</div>
      )}

      {createdLoan && (
        <div className="status success">
          Created loan {createdLoan.loanId} for member {createdLoan.memberId} and
          book {createdLoan.bookId}. Due date: {createdLoan.dueDate}. Total due:{" "}
          {formatCurrency(createdLoan.totalDue, createdLoan.currency)}.
        </div>
      )}
    </section>
  );
}

function BooksPage({
  availabilityFilter,
  booksError,
  booksLoading,
  clearFilters,
  form,
  formError,
  formMode,
  onCancelForm,
  onEdit,
  onFormChange,
  onSave,
  onStartAdd,
  onUpdateAvailability,
  onUpdateSearch,
  onUpdateUse,
  search,
  useFilter,
  visibleBooks,
}) {
  return (
    <section className="page" aria-labelledby="books-heading">
      <PageHeader
        id="books-heading"
        action={<button onClick={onStartAdd} type="button">Add book</button>}
        count={`${visibleBooks.length} books`}
        title="Books"
        subtitle="Manage book records and lending flags."
      />

      {formMode && (
        <BookForm
          error={formError}
          form={form}
          mode={formMode.type}
          onCancel={onCancelForm}
          onChange={onFormChange}
          onSave={onSave}
        />
      )}

      <div className="filters" aria-label="Book filters">
        <label>
          <span>Search</span>
          <input
            value={search}
            onChange={(event) => onUpdateSearch(event.target.value)}
            placeholder="Book ID or title"
          />
        </label>
        <label>
          <span>Availability</span>
          <select
            value={availabilityFilter}
            onChange={(event) => onUpdateAvailability(event.target.value)}
          >
            <option value="all">All</option>
            <option value="available">Available</option>
            <option value="unavailable">Unavailable</option>
          </select>
        </label>
        <label>
          <span>Use</span>
          <select value={useFilter} onChange={(event) => onUpdateUse(event.target.value)}>
            <option value="all">All</option>
            <option value="regular">Regular</option>
            <option value="reference">Reference only</option>
          </select>
        </label>
        <button className="secondary" onClick={clearFilters} type="button">
          Clear
        </button>
      </div>

      {booksLoading && <div className="status neutral">Loading book catalogue...</div>}
      {booksError && <div className="status error">Book catalogue error: {booksError}</div>}
      {!booksLoading && !booksError && visibleBooks.length === 0 && (
        <div className="status neutral">No books match the current view.</div>
      )}
      {!booksLoading && !booksError && visibleBooks.length > 0 && (
        <BooksTable books={visibleBooks} onEdit={onEdit} />
      )}
    </section>
  );
}

function MembersPage({
  clearFilters,
  form,
  formError,
  formMode,
  memberOverview,
  memberOverviewError,
  memberOverviewLoading,
  membersError,
  membersLoading,
  onCancelForm,
  onEdit,
  onFormChange,
  onOpenOverview,
  onSave,
  onStartAdd,
  onUpdateSearch,
  onUpdateSuspension,
  onUpdateType,
  search,
  suspensionFilter,
  typeFilter,
  visibleMembers,
}) {
  return (
    <section className="page" aria-labelledby="members-heading">
      <PageHeader
        id="members-heading"
        action={<button onClick={onStartAdd} type="button">Add member</button>}
        count={`${visibleMembers.length} members`}
        title="Members"
        subtitle="Manage members and open member overviews."
      />

      {formMode && (
        <MemberForm
          error={formError}
          form={form}
          mode={formMode.type}
          onCancel={onCancelForm}
          onChange={onFormChange}
          onSave={onSave}
        />
      )}

      <div className="filters" aria-label="Member filters">
        <label>
          <span>Search</span>
          <input
            value={search}
            onChange={(event) => onUpdateSearch(event.target.value)}
            placeholder="Member ID, name, or email"
          />
        </label>
        <label>
          <span>Type</span>
          <select value={typeFilter} onChange={(event) => onUpdateType(event.target.value)}>
            <option value="all">All</option>
            <option value="default">Default</option>
            <option value="student">Student</option>
            <option value="senior">Senior</option>
          </select>
        </label>
        <label>
          <span>Suspension</span>
          <select
            value={suspensionFilter}
            onChange={(event) => onUpdateSuspension(event.target.value)}
          >
            <option value="all">All</option>
            <option value="suspended">Suspended</option>
            <option value="not-suspended">Not suspended</option>
          </select>
        </label>
        <button className="secondary" onClick={clearFilters} type="button">
          Clear
        </button>
      </div>

      {membersLoading && <div className="status neutral">Loading member list...</div>}
      {membersError && <div className="status error">Member list error: {membersError}</div>}
      {!membersLoading && !membersError && visibleMembers.length === 0 && (
        <div className="status neutral">No members match the current view.</div>
      )}
      {!membersLoading && !membersError && visibleMembers.length > 0 && (
        <MembersTable
          members={visibleMembers}
          onEdit={onEdit}
          onOpenOverview={onOpenOverview}
        />
      )}

      {(memberOverviewLoading || memberOverviewError || memberOverview) && (
        <MemberOverview
          error={memberOverviewError}
          loading={memberOverviewLoading}
          overview={memberOverview}
        />
      )}
    </section>
  );
}

function LoansPage({
  clearFilters,
  dueFilter,
  loanReturnError,
  loanReturnLoadingId,
  loansError,
  loansLoading,
  onReturnLoan,
  onUpdateDue,
  onUpdateSearch,
  onUpdateStatus,
  returnedLoan,
  search,
  statusFilter,
  visibleLoans,
}) {
  return (
    <section className="page" aria-labelledby="loans-heading">
      <PageHeader
        id="loans-heading"
        count={`${visibleLoans.length} loans`}
        title="Loans"
        subtitle="Inspect active and returned loan activity."
      />

      <div className="filters" aria-label="Loan filters">
        <label>
          <span>Search</span>
          <input
            value={search}
            onChange={(event) => onUpdateSearch(event.target.value)}
            placeholder="Loan, book, or member ID"
          />
        </label>
        <label>
          <span>Status</span>
          <select value={statusFilter} onChange={(event) => onUpdateStatus(event.target.value)}>
            <option value="all">All</option>
            <option value="active">Active</option>
            <option value="returned">Returned</option>
          </select>
        </label>
        <label>
          <span>Due date</span>
          <select value={dueFilter} onChange={(event) => onUpdateDue(event.target.value)}>
            <option value="all">All</option>
            <option value="future">Due in future</option>
            <option value="today">Due today</option>
            <option value="overdue">Overdue</option>
            <option value="returned">Returned</option>
          </select>
        </label>
        <button className="secondary" onClick={clearFilters} type="button">
          Clear
        </button>
      </div>

      {loansLoading && <div className="status neutral">Loading loan list...</div>}
      {loansError && <div className="status error">Loan list error: {loansError}</div>}
      {loanReturnError && (
        <div className="status error">Loan return error: {loanReturnError}</div>
      )}
      {returnedLoan && (
        <div className="status success">
          Returned loan {returnedLoan.loanId}. Book {returnedLoan.bookId} is available again.
        </div>
      )}
      {!loansLoading && !loansError && visibleLoans.length === 0 && (
        <div className="status neutral">No loans match the current view.</div>
      )}
      {!loansLoading && !loansError && visibleLoans.length > 0 && (
        <LoansTable
          loans={visibleLoans}
          onReturnLoan={onReturnLoan}
          returningLoanId={loanReturnLoadingId}
        />
      )}
    </section>
  );
}

function BookForm({ error, form, mode, onCancel, onChange, onSave }) {
  return (
    <form className="record-form" onSubmit={onSave}>
      <h2>{mode === "edit" ? "Edit Book" : "Add Book"}</h2>
      <label>
        <span>Title</span>
        <input
          value={form.title}
          onChange={(event) => onChange({ ...form, title: event.target.value })}
        />
      </label>
      <label>
        <span>Category</span>
        <input
          value={form.category}
          onChange={(event) => onChange({ ...form, category: event.target.value })}
        />
      </label>
      <label className="checkbox-label">
        <input
          checked={form.available}
          onChange={(event) => onChange({ ...form, available: event.target.checked })}
          type="checkbox"
        />
        <span>Available</span>
      </label>
      <label className="checkbox-label">
        <input
          checked={form.referenceOnly}
          onChange={(event) =>
            onChange({ ...form, referenceOnly: event.target.checked })
          }
          type="checkbox"
        />
        <span>Reference only</span>
      </label>
      {error && <div className="status error">{error}</div>}
      <div className="form-actions">
        <button type="submit">Save</button>
        <button className="secondary" onClick={onCancel} type="button">
          Cancel
        </button>
      </div>
    </form>
  );
}

function MemberForm({ error, form, mode, onCancel, onChange, onSave }) {
  return (
    <form className="record-form" onSubmit={onSave}>
      <h2>{mode === "edit" ? "Edit Member" : "Add Member"}</h2>
      <label>
        <span>First name</span>
        <input
          value={form.firstName}
          onChange={(event) => onChange({ ...form, firstName: event.target.value })}
        />
      </label>
      <label>
        <span>Last name</span>
        <input
          value={form.lastName}
          onChange={(event) => onChange({ ...form, lastName: event.target.value })}
        />
      </label>
      <label>
        <span>Email</span>
        <input
          value={form.email}
          onChange={(event) => onChange({ ...form, email: event.target.value })}
          type="email"
        />
      </label>
      <label>
        <span>Type</span>
        <select
          value={form.memberType}
          onChange={(event) => onChange({ ...form, memberType: event.target.value })}
        >
          <option value="default">Default</option>
          <option value="student">Student</option>
          <option value="senior">Senior</option>
        </select>
      </label>
      <label>
        <span>Suspended until</span>
        <input
          type="date"
          value={form.suspendedUntil}
          onChange={(event) =>
            onChange({ ...form, suspendedUntil: event.target.value })
          }
        />
      </label>
      {error && <div className="status error">{error}</div>}
      <div className="form-actions">
        <button type="submit">Save</button>
        <button className="secondary" onClick={onCancel} type="button">
          Cancel
        </button>
      </div>
    </form>
  );
}

function BooksTable({ books, onEdit }) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th scope="col">Book ID</th>
            <th scope="col">Title</th>
            <th scope="col">Category</th>
            <th scope="col">Availability</th>
            <th scope="col">Status</th>
            <th scope="col">Use</th>
            <th scope="col">Manage</th>
          </tr>
        </thead>
        <tbody>
          {books.map((book) => (
            <tr key={book.bookId}>
              <td>{book.bookId}</td>
              <td className="title-cell">{book.title}</td>
              <td>{book.category}</td>
              <td>
                <Badge kind={book.available ? "success" : "muted"}>
                  {book.available ? "Available" : "Unavailable"}
                </Badge>
              </td>
              <td>
                <Badge kind={bookStatusKind(book)}>{bookStatusLabel(book)}</Badge>
              </td>
              <td>
                <Badge kind={book.referenceOnly ? "warning" : "neutral"}>
                  {book.referenceOnly ? "Reference only" : "Regular item"}
                </Badge>
              </td>
              <td>
                <button className="table-action" onClick={() => onEdit(book)} type="button">
                  Edit
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function MembersTable({ members, onEdit, onOpenOverview }) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th scope="col">Member ID</th>
            <th scope="col">Name</th>
            <th scope="col">Email</th>
            <th scope="col">Type</th>
            <th scope="col">Suspension</th>
            <th scope="col">Manage</th>
          </tr>
        </thead>
        <tbody>
          {members.map((member) => (
            <tr key={member.memberId}>
              <td>{member.memberId}</td>
              <td className="title-cell">
                {member.firstName} {member.lastName}
              </td>
              <td>{member.email}</td>
              <td>{member.memberType}</td>
              <td>
                <Badge kind={member.suspendedUntil ? "warning" : "success"}>
                  {member.suspendedUntil
                    ? `Suspended until ${member.suspendedUntil}`
                    : "Not suspended"}
                </Badge>
              </td>
              <td className="table-actions">
                <button
                  className="table-action"
                  onClick={() => onOpenOverview(member.memberId)}
                  type="button"
                >
                  Overview
                </button>
                <button
                  className="table-action secondary"
                  onClick={() => onEdit(member)}
                  type="button"
                >
                  Edit
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function LoansTable({ loans, onReturnLoan, returningLoanId }) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th scope="col">Loan ID</th>
            <th scope="col">Book ID</th>
            <th scope="col">Member ID</th>
            <th scope="col">Loan date</th>
            <th scope="col">Due date</th>
            <th scope="col">Return date</th>
            <th scope="col">Total due</th>
            <th scope="col">Status</th>
            {onReturnLoan && <th scope="col">Manage</th>}
          </tr>
        </thead>
        <tbody>
          {loans.map((loan) => (
            <tr key={loan.loanId}>
              <td>{loan.loanId}</td>
              <td>{loan.bookId}</td>
              <td>{loan.memberId}</td>
              <td>{loan.loanDate}</td>
              <td>{loan.dueDate}</td>
              <td>{loan.returnDate || "Not returned"}</td>
              <td>{formatCurrency(loan.totalDue, loan.currency)}</td>
              <td>
                <Badge kind={loan.status === "active" ? "warning" : "success"}>
                  {loan.status === "active" ? "Active" : "Returned"}
                </Badge>
              </td>
              {onReturnLoan && (
                <td>
                  {loan.status === "active" ? (
                    <button
                      className="table-action"
                      disabled={returningLoanId === loan.loanId}
                      onClick={() => onReturnLoan(loan)}
                      type="button"
                    >
                      {returningLoanId === loan.loanId ? "Returning..." : "Return"}
                    </button>
                  ) : (
                    <span className="quiet-text">Returned</span>
                  )}
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function MemberOverview({ error, loading, overview }) {
  return (
    <section className="member-overview" aria-labelledby="member-overview-heading">
      <div className="section-header">
        <h2 id="member-overview-heading">Member Overview</h2>
        {overview && <span className="count">{overview.loans.length} loans</span>}
      </div>

      {loading && <div className="status neutral">Loading member overview...</div>}
      {error && <div className="status error">Member overview error: {error}</div>}

      {!loading && !error && overview && (
        <div className="overview-layout">
          <div className="overview-details">
            <dl>
              <div>
                <dt>Member ID</dt>
                <dd>{overview.member.memberId}</dd>
              </div>
              <div>
                <dt>Name</dt>
                <dd>
                  {overview.member.firstName} {overview.member.lastName}
                </dd>
              </div>
              <div>
                <dt>Email</dt>
                <dd>{overview.member.email}</dd>
              </div>
              <div>
                <dt>Type</dt>
                <dd>{overview.member.memberType}</dd>
              </div>
              <div>
                <dt>Suspension</dt>
                <dd>
                  <Badge kind={overview.member.suspendedUntil ? "warning" : "success"}>
                    {overview.member.suspendedUntil
                      ? `Suspended until ${overview.member.suspendedUntil}`
                      : "Not suspended"}
                  </Badge>
                </dd>
              </div>
            </dl>
          </div>

          <div>
            {overview.loans.length === 0 ? (
              <div className="status neutral">No loans found for this member.</div>
            ) : (
              <LoansTable loans={overview.loans} />
            )}
          </div>
        </div>
      )}
    </section>
  );
}

function PageHeader({ action, count, id, subtitle, title }) {
  return (
    <header className="page-header">
      <div>
        <h1 id={id}>{title}</h1>
        <p>{subtitle}</p>
      </div>
      <div className="page-header-actions">
        {count && <span className="count">{count}</span>}
        {action}
      </div>
    </header>
  );
}

function Badge({ children, kind }) {
  return <span className={`badge ${kind}`}>{children}</span>;
}

function bookStatusLabel(book) {
  if (book.status === "lent") {
    return "Lent";
  }
  if (book.status === "reference-only") {
    return "Reference only";
  }
  if (book.status === "unavailable") {
    return "Unavailable";
  }
  return book.available ? "Available" : "Unavailable";
}

function bookStatusKind(book) {
  if (book.status === "lent" || book.status === "reference-only") {
    return "warning";
  }
  return book.available ? "success" : "muted";
}

function canLoanBook(book) {
  return book.available && !book.referenceOnly && book.status !== "lent";
}

function getInitialPage() {
  const candidate = window.location.hash.replace("#", "");
  return PAGE_LABELS[candidate] ? candidate : "lending";
}

function nextId(records, field, prefix) {
  const nextNumber =
    records.reduce((max, record) => {
      const raw = record[field] || "";
      const value = raw.startsWith(prefix) ? Number(raw.slice(1)) : 0;
      return Number.isFinite(value) ? Math.max(max, value) : max;
    }, 0) + 1;
  return `${prefix}${String(nextNumber).padStart(3, "0")}`;
}

function matchesDueFilter(loan, filter) {
  if (filter === "all") {
    return true;
  }
  if (filter === "returned") {
    return loan.status === "returned";
  }
  if (loan.status !== "active") {
    return false;
  }

  const today = new Date().toISOString().slice(0, 10);
  if (filter === "today") {
    return loan.dueDate === today;
  }
  if (filter === "overdue") {
    return loan.dueDate < today;
  }
  if (filter === "future") {
    return loan.dueDate > today;
  }
  return true;
}

function formatCurrency(value, currency = "EUR") {
  const amount = Number(value || 0);
  return `${amount.toFixed(2)} ${currency}`;
}

export default App;
