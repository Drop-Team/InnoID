import { Tokens } from "@/lib/objects";
import { cookies } from "next/dist/client/components/headers";

export class LocalStorage {
  getAccessToken(): string | null {
    return localStorage.getItem("access_token");
  }

  getRefreshToken(): string | null {
    return localStorage.getItem("refresh_token");
  }

  setAccessToken(token: string) {
    localStorage.setItem("access_token", token);
  }

  setRefreshToken(token: string) {
    localStorage.setItem("refresh_token", token);
  }
}
  

// export class CookieStorageGetter {
//   private access_token: string | undefined;
//   private refresh_token: string | undefined;

//   constructor(cookies: object) {
//     this.access_token = cookies.access_token;
//     this.refresh_token = cookies.refresh_token;
//   }

//   getAccessToken(): string | undefined {
//     return this.access_token;
//   }

//   getRefreshToken(): string | undefined {
//     return this.refresh_token;
//   }
// }

// export class CookieStorageSetter {
//   setAccessToken(token: string) {
//     document.cookie = `access_token=${token}; path=/;`;
//   }

//   setRefreshToken(token: string) {
//     document.cookie = `refresh_token=${token}; path=/;`;
//   }

// // export class CookieStorage {
// //   access_token: string | undefined;
// //   refresh_token: string | undefined;

// //   constructor(cookies: object) {
// //     this.access_token = cookies.access_token;
// //     this.refresh_token = cookies.refresh_token;
// //   }

// //   static setTokens(tokens: Tokens) {
// //     // localStorage.setItem("access_token", tokens.access_token);
// //     // localStorage.setItem("refresh_token", tokens.refresh_token);
// //     document.cookie = `access_token=${tokens.access_token}; path=/;`;
// //   }

// //   static getTokens(): Tokens {
// //     return {
// //       access_token: localStorage.getItem("access_token") || "",
// //       refresh_token: localStorage.getItem("refresh_token") || "",
// //     };
// //   }
// // }
