CREATE TABLE "tbs_approvaldonaterequest" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"request_date" datetime NOT NULL, 
	"request_expiration" datetime NOT NULL, 
	"donor_id" integer NOT NULL REFERENCES "auth_user" ("id")
);

CREATE TABLE "tbs_approvalsellrequest" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"request_date" datetime NOT NULL, 
	"request_expiration" datetime NOT NULL
);


CREATE TABLE "tbs_category" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"category_name" varchar(30) NOT NULL
);
CREATE TABLE "tbs_item" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"name" varchar(50) NOT NULL, 
	"description" varchar(500) NOT NULL, 
	"status" varchar(15) NOT NULL, 
	"purpose" varchar(10) NOT NULL, 
	"price" real NOT NULL, 
	"stars_to_use" integer NOT NULL, 
	"picture" varchar(200) NOT NULL, 
	"stars_required" integer NOT NULL, 
	"date_approved" datetime NULL, 
	"category_id" integer NULL REFERENCES 
	"tbs_category" ("id")
);
CREATE TABLE "tbs_notification" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"message" varchar(500) NOT NULL, 
	"notification_type" varchar(10) NOT NULL, 
	"status" varchar(10) NOT NULL, 
	"notification_date" datetime NOT NULL, 
	"notification_expiration" datetime NOT NULL, 
	"item_id" integer NOT NULL REFERENCES "tbs_item" ("id"), 
	"maker_id" integer NOT NULL REFERENCES "auth_user" ("id"), 
	"target_id" integer NOT NULL REFERENCES "auth_user" ("id")
);
CREATE TABLE "tbs_reservationrequest" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"reserved_date" datetime NOT NULL, 
	"request_expiration" datetime NOT NULL, 
	"status" varchar(10) NOT NULL, 
	"buyer_id" integer NOT NULL REFERENCES "auth_user" ("id"), 
	"item_id" integer NOT NULL UNIQUE REFERENCES "tbs_item" ("id")
);
CREATE TABLE "tbs_student" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"id_number" varchar(50) NOT NULL, 
	"first_name" varchar(255) NOT NULL, 
	"last_name" varchar(255) NOT NULL, 
	"course" varchar(100) NOT NULL
);
CREATE TABLE "tbs_transaction" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"date_claimed" datetime NOT NULL
);
CREATE TABLE "tbs_userprofile" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"stars_collected" integer NOT NULL, 
	"student_id" integer NOT NULL UNIQUE REFERENCES "tbs_student" ("id"), 
	"user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id")
);
CREATE TABLE "tbs_transaction__new" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"date_claimed" datetime NOT NULL, 
	"buyer_id" integer NOT NULL REFERENCES "tbs_userprofile" ("id")
);
INSERT INTO "tbs_transaction__new" ("date_claimed", "id", "buyer_id") 
	SELECT "date_claimed", "id", NULL FROM "tbs_transaction";
DROP TABLE "tbs_transaction";

ALTER TABLE "tbs_transaction__new" RENAME TO "tbs_transaction";

CREATE INDEX "tbs_approvaldonaterequest_029df19e" ON "tbs_approvaldonaterequest" ("donor_id");

CREATE INDEX "tbs_item_b583a629" ON "tbs_item" ("category_id");

CREATE INDEX "tbs_notification_82bfda79" ON "tbs_notification" ("item_id");

CREATE INDEX "tbs_notification_8e8bc641" ON "tbs_notification" ("maker_id");

CREATE INDEX "tbs_notification_55e2df16" ON "tbs_notification" ("target_id");

CREATE INDEX "tbs_reservationrequest_2c724d65" ON "tbs_reservationrequest" ("buyer_id");

CREATE INDEX "tbs_transaction_2c724d65" ON "tbs_transaction" ("buyer_id");

CREATE TABLE "tbs_transaction__new" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"date_claimed" datetime NOT NULL, 
	"buyer_id" integer NOT NULL REFERENCES "tbs_userprofile" ("id"), 
	"item_id" integer NOT NULL UNIQUE REFERENCES "tbs_item" ("id")
);
INSERT INTO "tbs_transaction__new" ("item_id", "date_claimed", "id", "buyer_id") SELECT NULL, "date_claimed", "id", "buyer_id" FROM "tbs_transaction";

DROP TABLE "tbs_transaction";

ALTER TABLE "tbs_transaction__new" RENAME TO "tbs_transaction";

CREATE INDEX "tbs_transaction_2c724d65" ON "tbs_transaction" ("buyer_id");

CREATE TABLE "tbs_transaction__new" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"date_claimed" datetime NOT NULL, 
	"buyer_id" integer NOT NULL REFERENCES "tbs_userprofile" ("id"), 
	"item_id" integer NOT NULL UNIQUE REFERENCES "tbs_item" ("id"), 
	"seller_id" integer NOT NULL REFERENCES "tbs_userprofile" ("id")
);
INSERT INTO "tbs_transaction__new" ("item_id", "seller_id", "date_claimed", "id", "buyer_id") 
	SELECT "item_id", NULL, "date_claimed", "id", "buyer_id" FROM "tbs_transaction";

DROP TABLE "tbs_transaction";

ALTER TABLE "tbs_transaction__new" RENAME TO "tbs_transaction";

CREATE INDEX "tbs_transaction_2c724d65" ON "tbs_transaction" ("buyer_id");

CREATE INDEX "tbs_transaction_0a7c7ff2" ON "tbs_transaction" ("seller_id");

CREATE TABLE "tbs_item__new" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"name" varchar(50) NOT NULL, 
	"description" varchar(500) NOT NULL, 
	"status" varchar(15) NOT NULL, 
	"purpose" varchar(10) NOT NULL, 
	"price" real NOT NULL, 
	"stars_to_use" integer NOT NULL, 
	"picture" varchar(200) NOT NULL, 
	"stars_required" integer NOT NULL, 
	"date_approved" datetime NULL, 
	"category_id" integer NULL REFERENCES "tbs_category" ("id"), 
	"owner_id" integer NOT NULL REFERENCES "tbs_userprofile" ("id")
);
INSERT INTO "tbs_item__new" ("date_approved", "category_id", "picture", "id", "stars_to_use", "owner_id", "purpose", "name", "stars_required", "price", "description", "status") SELECT "date_approved", "category_id", "picture", "id", "stars_to_use", NULL, "purpose", "name", "stars_required", "price", "description", "status" FROM "tbs_item";

DROP TABLE "tbs_item";

ALTER TABLE "tbs_item__new" RENAME TO "tbs_item";

CREATE INDEX "tbs_item_b583a629" ON "tbs_item" ("category_id");

CREATE INDEX "tbs_item_5e7b1936" ON "tbs_item" ("owner_id");

CREATE TABLE "tbs_approvalsellrequest__new" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"request_date" datetime NOT NULL, 
	"request_expiration" datetime NOT NULL, 
	"item_id" integer NOT NULL UNIQUE REFERENCES "tbs_item" ("id")
);
INSERT INTO "tbs_approvalsellrequest__new" ("item_id", "request_date", "request_expiration", "id") SELECT NULL, "request_date", "request_expiration", "id" FROM "tbs_approvalsellrequest";

DROP TABLE "tbs_approvalsellrequest";

ALTER TABLE "tbs_approvalsellrequest__new" RENAME TO "tbs_approvalsellrequest";

CREATE TABLE "tbs_approvalsellrequest__new" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"request_date" datetime NOT NULL, 
	"request_expiration" datetime NOT NULL, 
	"item_id" integer NOT NULL UNIQUE REFERENCES "tbs_item" ("id"), 
	"seller_id" integer NOT NULL REFERENCES "auth_user" ("id")
);
INSERT INTO "tbs_approvalsellrequest__new" ("item_id", "seller_id", "request_date", "request_expiration", "id") SELECT "item_id", NULL, "request_date", "request_expiration", "id" FROM "tbs_approvalsellrequest";

DROP TABLE "tbs_approvalsellrequest";

ALTER TABLE "tbs_approvalsellrequest__new" RENAME TO "tbs_approvalsellrequest";

CREATE INDEX "tbs_approvalsellrequest_0a7c7ff2" ON "tbs_approvalsellrequest" ("seller_id");

CREATE TABLE "tbs_approvaldonaterequest__new" (
	"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	"request_date" datetime NOT NULL, 
	"request_expiration" datetime NOT NULL, 
	"donor_id" integer NOT NULL REFERENCES "auth_user" ("id"), 
	"item_id" integer NOT NULL UNIQUE REFERENCES "tbs_item" ("id")
);
INSERT INTO "tbs_approvaldonaterequest__new" ("item_id", "donor_id", "request_date", "request_expiration", "id") SELECT NULL, "donor_id", "request_date", "request_expiration", "id" FROM "tbs_approvaldonaterequest";

DROP TABLE "tbs_approvaldonaterequest";

ALTER TABLE "tbs_approvaldonaterequest__new" RENAME TO "tbs_approvaldonaterequest";

CREATE INDEX "tbs_approvaldonaterequest_029df19e" ON "tbs_approvaldonaterequest" ("donor_id");