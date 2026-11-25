// My account: who you are, and for drivers their details, cars and reviews.
(async function account() {
  const saved = auth.require();
  if (!saved) return;
  const loading = document.getElementById("loading");
  const msg = document.getElementById("msg");
  const ROLES = { passenger: "Traveller", driver: "Driver", admin: "Admin" };
  const STATUS = {
    approved: ["Approved driver", "is-good"],
    pending: ["Waiting for approval", ""],
    rejected: ["Not approved", "is-bad"],
  };

  try {
    const { user } = await api.get("/auth/me");
    showProfile(user);
    if (user.role === "driver") await showDriver();
    showActions(user.role);
  } catch (err) {
    ui.say(msg, err.message);
  } finally {
    loading.hidden = true;
  }

  function showProfile(u) {
    const box = document.getElementById("profile");
    box.append(
      ui.el("span", "profile-name", u.full_name),
      ui.el("span", "profile-meta", `${ROLES[u.role]} · 0${u.phone.slice(4)}`),
    );
    if (u.email) box.append(ui.el("span", "profile-meta", u.email));
    box.append(ui.el("span", "profile-meta", `Member since ${ui.date(u.created_at)}`));
    if (u.driver) {
      const [label, tone] = STATUS[u.driver.status] || STATUS.pending;
      box.append(ui.el("span", `badge ${tone}`, label));
    }
  }

  async function showDriver() {
    const [{ documents, details, driver }, { vehicles }] = await Promise.all([
      api.get("/drivers/documents"), api.get("/drivers/vehicles")]);

    const missing = documents.filter((d) => !d.uploaded || d.expired).length;
    const facts = [
      ["Rating", driver.avg_rating ? `★ ${driver.avg_rating.toFixed(1)}` : "No reviews yet"],
      ["Home", [details.home_sector, details.home_district].filter(Boolean).join(", ")],
      ["Date of birth", details.date_of_birth && ui.date(details.date_of_birth)],
      ["Gender", details.gender && details.gender[0].toUpperCase() + details.gender.slice(1)],
      ["National ID", details.national_id_number && `•••• ${details.national_id_number.slice(-4)}`],
      ["Driving licence", details.license_number],
      ["Documents", missing ? `${missing} of ${documents.length} still to upload`
        : `All ${documents.length} uploaded`],
    ];
    if (driver.rejection_reason) facts.push(["Reason", driver.rejection_reason]);
    document.getElementById("facts").replaceChildren(...facts.flatMap(([k, v]) =>
      [ui.el("dt", null, k), ui.el("dd", null, v || "Not filled in")]));
    document.getElementById("driver-block").hidden = false;

    if (vehicles.length) {
      document.getElementById("cars").replaceChildren(...vehicles.map(carRow));
      document.getElementById("cars-block").hidden = false;
    }

    if (driver.status === "approved") {
      try {
        const said = await api.get(`/drivers/${driver.driver_id}/ratings`);
        document.getElementById("reviews").replaceChildren(
          ui.reviews(said, { empty: "No reviews yet." }));
      } catch (err) {
        // Reviews are a nice extra here.
      }
    }
  }

  function carRow(v) {
    const li = ui.el("li", "result car-row");
    if (v.photos.length) {
      const img = ui.el("img");
      img.src = v.photos[0].url;
      img.alt = v.model;
      li.append(img);
    }
    const text = ui.el("div");
    text.append(
      ui.el("strong", null, `${v.colour || ""} ${v.model}${v.year ? `, ${v.year}` : ""}`.trim()),
      ui.el("div", "result-meta",
        `${v.plate_number} · ${v.seats} passenger seats${v.has_ac ? " · AC" : ""}`),
    );
    li.append(text);
    return li;
  }

  function showActions(role) {
    const box = document.getElementById("actions");
    const link = (href, text, cls = "btn-gray btn-sm") => {
      const a = ui.el("a", cls, text);
      a.href = href;
      box.append(a);
    };
    if (role === "driver") {
      link("/driver/offer.html", "My trips", "btn-black btn-sm");
      link("/driver/offer.html#setup", "Edit details, documents and cars");
    } else if (role === "passenger") {
      link("/bookings.html", "My bookings", "btn-black btn-sm");
      link("/", "Find a trip");
    } else {
      link("/admin/drivers.html", "Drivers", "btn-black btn-sm");
    }
    const out = ui.el("button", "btn-gray btn-sm", "Log out");
    out.type = "button";
    out.addEventListener("click", auth.logout);
    box.append(out);
  }
})();
