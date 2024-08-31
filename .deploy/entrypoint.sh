#!/usr/bin/env sh

envsubst_inplace() {
  file=$1
  tmpfile=$(mktemp)
  EXISTING_VARS=$(printenv | awk -F= '{print $1}' | sed 's/^/\$/g' | paste -sd,)
  # unavailable for alpine
  # cp --attributes-only --preserve "${file}" "${tmpfile}"
  envsubst "${EXISTING_VARS}" < "${file}" | tee "${tmpfile}" >/dev/null
  cat "${tmpfile}" > "${file}"
}

if [[ -z "${JS_FILES}" ]]; then
  echo 'Please, set $JS_FILES environment variable to point to build files javascript root'
  exit 1
fi

# Replace environment variables in built frontend files
for file in $JS_FILES;
do
  envsubst_inplace "${file}" 2> /dev/null
done

if [[ -z "${HTML_FILES}" ]]; then
  echo 'Please, set $HTML_FILES environment variable to point to build files html root'
  exit 1
fi

# Replace environment variables in built frontend files
for file in $HTML_FILES;
do
  envsubst_inplace "${file}" 2> /dev/null
done

echo "Running nginx"

# Run nginx
nginx -g "daemon off;"
